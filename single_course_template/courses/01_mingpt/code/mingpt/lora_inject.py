import itertools
import types
import mindspore as ms
from mindspore import nn
from mindspore import mint
from mindspore.common.initializer import initializer, Normal

_UID = itertools.count()

class LoRADense(nn.Cell):
    """
    y = base(x) + scale * ( (drop(x) @ A^T) @ B^T )
    """
    class Params(nn.Cell):
        def __init__(self, in_dim, out_dim, r):
            super().__init__()
            self.A = ms.Parameter(initializer(Normal(0.0, 1.0), (r, in_dim)), name="A")
            self.B = ms.Parameter(mint.zeros((out_dim, r)), name="B")

    def __init__(self, base: nn.Dense, r=8, alpha=16.0, dropout=0.0):
        super().__init__()
        self.base = base
        in_dim, out_dim = int(base.in_channels), int(base.out_channels)
        setattr(self, f"lora_{next(_UID)}", self.Params(in_dim, out_dim, r))
        self.scale = alpha / r
        self.drop = nn.Dropout(p=dropout) if dropout > 0 else None
        for p in self.base.get_parameters():
            p.requires_grad = False

    def get_lora_params(self):
        for n, cell in self.cells_and_names():
            if isinstance(cell, self.Params):
                return cell.A, cell.B

    def construct(self, x):
        y = self.base(x)
        x_eff = self.drop(x) if self.drop else x
        A, B = self.get_lora_params()
        return y + self.scale * mint.matmul(mint.matmul(x_eff, A.T), B.T)


def inject_lora_into_gpt(model, r=8, alpha=16.0, dropout=0.0,
                         target=("qkv","attn_out","mlp"), include_lm_head=False):
    """注入LoRA（qkv/attn_out/mlp）"""
    for block in model.h:
        if "qkv" in target and isinstance(block.attn.c_attn, nn.Dense):
            block.attn.c_attn = LoRADense(block.attn.c_attn, r, alpha, dropout)
        if "attn_out" in target and isinstance(block.attn.c_proj, nn.Dense):
            block.attn.c_proj = LoRADense(block.attn.c_proj, r, alpha, dropout)
        if "mlp" in target:
            if "c_fc" in block.mlp and isinstance(block.mlp["c_fc"], nn.Dense):
                block.mlp["c_fc"] = LoRADense(block.mlp["c_fc"], r, alpha, dropout)
            if "c_proj" in block.mlp and isinstance(block.mlp["c_proj"], nn.Dense):
                block.mlp["c_proj"] = LoRADense(block.mlp["c_proj"], r, alpha, dropout)
    if include_lm_head and isinstance(model.lm_head, nn.Dense):
        model.lm_head = LoRADense(model.lm_head, r, alpha, dropout)

def mark_only_lora_as_trainable(model, allow=()):
    """只训练.lora_参数"""
    for n, p in model.parameters_and_names():
        if p is None:
            continue
        p.requires_grad = (".lora_" in n) or any(k in n for k in allow)

def attach_lora_optimizer(model):
    """替换configure_optimizers，让优化器只更新LoRA参数"""
    def _configure_optimizers_lora(self, cfg):
        lora_params = [p for n, p in self.parameters_and_names() if p is not None and ".lora_" in n]
        for n, p in self.parameters_and_names():
            if p is not None and ".lora_" not in n:
                p.requires_grad = False
        return nn.AdamWeightDecay(
            [{"params": lora_params, "weight_decay": 0.0}],
            learning_rate=cfg.learning_rate,
            beta1=cfg.betas[0], beta2=cfg.betas[1], eps=1e-8
        )
    model.configure_optimizers = types.MethodType(_configure_optimizers_lora, model)

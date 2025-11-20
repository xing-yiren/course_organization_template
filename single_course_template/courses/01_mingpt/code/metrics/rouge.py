import numpy as np
import mindspore as ms
from rouge_score import rouge_scorer

_SCORER = rouge_scorer.RougeScorer(['rouge1','rouge2','rougeL'], use_stemmer=True)

def eval_rouge(model, val_ids, tok, samples=5, ctx=64, gen=64, stride=256):
    """在验证集上，用rouge_scorer计算ROUGE-1/L"""
    model.set_train(False)
    res, pos = [], 0

    for _ in range(samples):
        if pos + ctx + gen > len(val_ids):
            break

        # 准备上下文与参考
        ctx_ids = val_ids[pos:pos+ctx]
        ref_ids = val_ids[pos+ctx:pos+ctx+gen]
        pos += stride

        # 生成
        x = ms.Tensor([ctx_ids], ms.int32)
        hyp_ids = model.generate(x, max_new_tokens=gen, do_sample=False).asnumpy()[0][-gen:]

        # BPE decode到字符串后计算ROUGE
        ref = tok.decode(ms.Tensor(ref_ids, ms.int32))
        hyp = tok.decode(ms.Tensor(hyp_ids, ms.int32))

        s = _SCORER.score(ref, hyp)
        res.append((s['rouge1'].fmeasure, s['rouge2'].fmeasure, s['rougeL'].fmeasure))

    model.set_train(True)

    if not res:
        return 0.0, 0.0, 0.0
    arr = np.array(res, dtype=np.float32)
    return float(arr[:,0].mean()), float(arr[:,1].mean()), float(arr[:,2].mean())

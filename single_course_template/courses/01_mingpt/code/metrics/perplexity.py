import math
from mindspore import mint
from mindspore.dataset import GeneratorDataset

def evaluate_model(model, val_dataset, block_size=256, batch_size=8):
    """
    在验证集上计算平均 loss 和 perplexity
    """
    model.set_train(False)

    val_loader = GeneratorDataset(
        val_dataset,
        column_names=["x", "y"],
        shuffle=False,
        num_parallel_workers=2,
    ).batch(batch_size, drop_remainder=True)

    total_loss, count = 0.0, 0
    for x, y in val_loader.create_tuple_iterator():
        logits = model(x).float()
        loss = mint.nn.functional.cross_entropy(
            logits.view(-1, logits.shape[-1]),
            y.view(-1),
            ignore_index=-1
        )
        total_loss += float(loss.asnumpy())
        count += 1

    avg_loss = total_loss / count if count > 0 else 1e9
    ppl = math.exp(avg_loss)
    return avg_loss, ppl

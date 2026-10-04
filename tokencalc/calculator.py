"""根据 token 数与价格表计算成本，并做多模型对比。

⚠️ 成本基于启发式 token 估算与快照价格，仅作量级参考。
"""

from __future__ import annotations

from typing import List

from .prices import PriceTable


def cost_for_model(model: dict, input_tokens: int, output_tokens: int) -> dict:
    """按单个模型价格算成本（美元）。"""
    input_cost = input_tokens / 1_000_000 * model["input_per_1m"]
    output_cost = output_tokens / 1_000_000 * model["output_per_1m"]
    return {
        "id": model["id"],
        "provider": model.get("provider", ""),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": input_cost + output_cost,
    }


def compare(price_table: PriceTable, input_tokens: int, output_tokens: int) -> List[dict]:
    """对价格表里所有模型算一遍成本，按总成本升序返回。"""
    rows = [cost_for_model(m, input_tokens, output_tokens) for m in price_table.list_models()]
    rows.sort(key=lambda r: r["total_cost"])
    return rows

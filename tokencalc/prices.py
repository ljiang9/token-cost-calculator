"""加载内置模型价格表（JSON）。

⚠️ 价格为快照，实际以官方定价为准。
"""

from __future__ import annotations

import json
import os
from typing import Dict, List

_DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "models.json")


class PriceTable:
    def __init__(self, models: List[dict], meta: dict | None = None):
        self.models = models
        self.meta = meta or {}
        self._by_id: Dict[str, dict] = {m["id"]: m for m in models}

    @staticmethod
    def load(path: str = _DATA_FILE) -> "PriceTable":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return PriceTable(models=data.get("models", []), meta=data.get("_meta", {}))

    def list_models(self) -> List[dict]:
        return self.models

    def get(self, model_id: str) -> dict:
        if model_id not in self._by_id:
            raise KeyError(f"价格表里没有模型：{model_id}")
        return self._by_id[model_id]

    def has(self, model_id: str) -> bool:
        return model_id in self._by_id

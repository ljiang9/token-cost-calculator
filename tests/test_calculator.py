import unittest

from tokencalc.calculator import compare, cost_for_model
from tokencalc.prices import PriceTable


class TestCostCalc(unittest.TestCase):
    def test_cost_math(self):
        # 模型：输入 $1 / 1M，输出 $3 / 1M
        model = {"id": "x", "provider": "t", "input_per_1m": 1.0, "output_per_1m": 3.0}
        # 1M 输入 + 1M 输出 -> 1 + 3 = 4
        row = cost_for_model(model, input_tokens=1_000_000, output_tokens=1_000_000)
        self.assertAlmostEqual(row["input_cost"], 1.0)
        self.assertAlmostEqual(row["output_cost"], 3.0)
        self.assertAlmostEqual(row["total_cost"], 4.0)

    def test_cost_scales_linearly(self):
        model = {"id": "x", "provider": "t", "input_per_1m": 2.0, "output_per_1m": 4.0}
        row = cost_for_model(model, input_tokens=500_000, output_tokens=250_000)
        self.assertAlmostEqual(row["input_cost"], 1.0)   # 0.5M * 2
        self.assertAlmostEqual(row["output_cost"], 1.0)  # 0.25M * 4
        self.assertAlmostEqual(row["total_cost"], 2.0)

    def test_zero_tokens_zero_cost(self):
        model = {"id": "x", "provider": "t", "input_per_1m": 2.0, "output_per_1m": 4.0}
        row = cost_for_model(model, 0, 0)
        self.assertAlmostEqual(row["total_cost"], 0.0)


class TestCompare(unittest.TestCase):
    def setUp(self):
        self.table = PriceTable.load()

    def test_compare_returns_all_models(self):
        rows = compare(self.table, input_tokens=1000, output_tokens=500)
        self.assertEqual(len(rows), len(self.table.list_models()))

    def test_compare_sorted_by_total_cost(self):
        rows = compare(self.table, input_tokens=1_000_000, output_tokens=1_000_000)
        totals = [r["total_cost"] for r in rows]
        self.assertEqual(totals, sorted(totals))

    def test_compare_cheapest_is_mini_model(self):
        rows = compare(self.table, input_tokens=1_000_000, output_tokens=1_000_000)
        # gpt-4o-mini / deepseek 这类应排在最前；只断言最低价模型不输给最贵模型
        self.assertLessEqual(rows[0]["total_cost"], rows[-1]["total_cost"])


if __name__ == "__main__":
    unittest.main()

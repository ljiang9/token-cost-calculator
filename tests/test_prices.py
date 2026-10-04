import unittest

from tokencalc.prices import PriceTable


class TestPriceTable(unittest.TestCase):
    def setUp(self):
        self.table = PriceTable.load()

    def test_loads_builtin_models(self):
        ids = [m["id"] for m in self.table.list_models()]
        self.assertIn("gpt-4o-mini", ids)
        self.assertIn("deepseek-chat", ids)
        self.assertGreaterEqual(len(ids), 5)

    def test_each_model_has_required_fields(self):
        for m in self.table.list_models():
            self.assertIn("input_per_1m", m)
            self.assertIn("output_per_1m", m)
            self.assertGreater(m["input_per_1m"], 0)
            self.assertGreater(m["output_per_1m"], 0)

    def test_get_existing_model(self):
        m = self.table.get("gpt-4o")
        self.assertEqual(m["id"], "gpt-4o")

    def test_get_missing_model_raises(self):
        with self.assertRaises(KeyError):
            self.table.get("no-such-model-xyz")

    def test_has(self):
        self.assertTrue(self.table.has("gpt-4o-mini"))
        self.assertFalse(self.table.has("nope"))

    def test_meta_present(self):
        # 价格快照说明应保留在 meta 里
        self.assertIn("note", self.table.meta)


if __name__ == "__main__":
    unittest.main()

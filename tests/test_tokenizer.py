import unittest

from tokencalc.tokenizer import estimate_tokens, WORDS_PER_TOKEN


class TestHeuristicTokenizer(unittest.TestCase):
    def test_pure_chinese(self):
        # 8 个汉字，0 个英文词
        r = estimate_tokens("这是一个中文句子")
        self.assertEqual(r["cjk_chars"], 8)
        self.assertEqual(r["latin_words"], 0)
        self.assertEqual(r["total"], 8)

    def test_chinese_punctuation_counts_as_cjk(self):
        r = estimate_tokens("你好，世界！")
        # 你好世界=4 汉字 + ，！=2 标点 = 6
        self.assertEqual(r["cjk_chars"], 6)
        self.assertEqual(r["total"], 6)

    def test_pure_english(self):
        # "hello world this is a test" -> 6 words
        r = estimate_tokens("hello world this is a test")
        self.assertEqual(r["latin_words"], 6)
        self.assertEqual(r["cjk_chars"], 0)
        self.assertEqual(r["latin_tokens"], round(6 * WORDS_PER_TOKEN))
        self.assertEqual(r["total"], r["latin_tokens"])

    def test_mixed_chinese_english(self):
        # "你好 world" -> 2 汉字 + 1 个英文词
        r = estimate_tokens("你好 world")
        self.assertEqual(r["cjk_chars"], 2)
        self.assertEqual(r["latin_words"], 1)
        self.assertEqual(r["total"], 2 + round(1 * WORDS_PER_TOKEN))

    def test_numbers_count_as_word(self):
        # price/is/12345/dollars = 4 个词
        r = estimate_tokens("price is 12345 dollars")
        self.assertEqual(r["latin_words"], 4)

    def test_empty_text(self):
        r = estimate_tokens("")
        self.assertEqual(r["total"], 0)


if __name__ == "__main__":
    unittest.main()

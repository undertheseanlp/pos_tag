# -*- coding: utf-8 -*-
from unittest import TestCase
from pipelines.data_preparation.convert_to_ud import extract_tokens


class TestExtractTokens(TestCase):
    def test_extract_tokens_1(self):
        tokens = extract_tokens("Hành_trình/N")
        self.assertEqual(tokens, ["Hành_trình", "N"])

    def test_extract_tokens_2(self):
        tokens = extract_tokens(",/CH")
        self.assertEqual(tokens, [",", "CH"])

    def test_extract_tokens_3(self):
        tokens = extract_tokens("//CH")
        self.assertEqual(tokens, ["/", "CH"])

    def test_extract_tokens_4(self):
        tokens = extract_tokens("!/!\"/CH")
        self.assertEqual(tokens, ["!/!\"", "CH"])



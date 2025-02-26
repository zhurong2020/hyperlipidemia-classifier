import unittest
from src.classifier import classify_hyperlipidemia

class TestClassifier(unittest.TestCase):
    def test_high_ldl(self):
        result = classify_hyperlipidemia(5.0, 6.0, 1.1, 1.5)
        self.assertIn("High Risk", result)

    def test_normal_levels(self):
        result = classify_hyperlipidemia(2.5, 4.5, 1.2, 1.4)
        self.assertIn("Normal", result)

if __name__ == '__main__':
    unittest.main() 
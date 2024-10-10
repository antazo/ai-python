import unittest
from template import interstitial

class TestTemplate(unittest.TestCase):
    def test_interstitial(self):
        self.assertEqual(interstitial(), "Hello Alex!")

if __name__ == '__main__':
    unittest.main()
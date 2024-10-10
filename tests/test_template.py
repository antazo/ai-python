import unittest
from ..py.template import interstitial

class TestTemplate(unittest.TestCase):
    def test_interstitial(self):
        self.assertEqual(interstitial(), "Hello, World!")

if __name__ == '__main__':
    unittest.main()
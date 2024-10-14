import unittest
from py.app import app

class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_default(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello', response.data)

    def test_hello_with_name(self):
        response = self.app.get('/?name=Juan')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Juan', response.data)

    def test_bye(self):
        response = self.app.get('/bye')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Goodbye Alex!', response.data)

    def test_bye_with_name(self):
        response = self.app.get('/bye?name=Torpedo')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Goodbye Torpedo!', response.data)

    def test_planet_distances(self):
        response = self.app.get('/planet_distances')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mercury', response.data)

    def test_foobar(self):
        response = self.app.get('/foobar')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'foobar', response.data)

    def test_non_existent_route(self):
        response = self.app.get('/non_existent_route')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
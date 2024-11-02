import unittest
from app import app
import pytest

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_default(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello', response.data)

    def test_non_existent_route(self):
        response = self.app.get('/non_existent_route')
        self.assertEqual(response.status_code, 404)

class TestOthers(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_planet_distances(self):
        response = self.app.get('/planet_distances')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mercury', response.data)

class TestFoobar(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_foobar(self):
        response = self.app.get('/foobar')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'foobar', response.data)

class TestHello(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_hello(self):
        response = self.app.get('/hello')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello', response.data)

    def test_hello_with_name(self):
        response = self.app.get('/hello?name=Juan')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Juan', response.data)

class TestBye(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_bye(self):
        response = self.app.get('/bye')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Goodbye', response.data)

    def test_bye_with_name(self):
        response = self.app.get('/bye?name=Torpedo')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Torpedo', response.data)

class TestGame(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_game(self):
        response = self.app.get('/game')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Game', response.data)

    def test_game_with_invalid_parameter(self):
        response = self.app.get('/game?choice=invalid')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Game', response.data)

class TestCognitiveServices(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_translator(self):
        response = self.app.get('/translator')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Translator', response.data)

    def test_computer_vision(self):
        response = self.app.get('/computer_vision')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Computer Vision', response.data)

    def test_face(self):
        response = self.app.get('/face')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Face', response.data)

if __name__ == '__main__':
    unittest.main()
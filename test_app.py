#!/usr/bin/env python3
# test_app.py

import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_default(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello', response.data)

    def test_home_with_name(self):
        response = self.app.get('/?name=Alex')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello Alex', response.data)

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

    def test_vision(self):
        response = self.app.get('/vision')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Vision', response.data)

    def test_face(self):
        response = self.app.get('/face')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Face', response.data)

if __name__ == '__main__':
    unittest.main()
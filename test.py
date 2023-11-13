from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('plays'))

    def test_valid_word(self):
        """Test if a word is valid by premaking a board"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "M", "O", "O", "N"], 
                                 ["C", "M", "O", "O", "N"], 
                                 ["C", "M", "O", "O", "N"], 
                                 ["C", "M", "O", "O", "N"], 
                                 ["C", "M", "O", "O", "N"]]
        response = self.client.get('/check-word?word=moon')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/check-word?word=card')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=awef')
        self.assertEqual(response.json['result'], 'not-word')

    def test_points(self):
        "Test if points in session updates"
        with self.client as client:
            with client.session_transaction() as sess:
                sess['highscore'] = 6
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['highscore'], 6)
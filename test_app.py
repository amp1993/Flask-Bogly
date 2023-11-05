import unittest
from app import app, db, connect_db
from models import User, Post, Tag
import os

app.config['TESTING'] = True
app.config['DEBUG_TB_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'

class BloglyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        # Set up the database
        connect_db(app)
        db.create_all()

    def tearDown(self):
        # Clean up the database after each test
        db.session.remove()
        db.drop_all()

    def test_homepage_redirect(self):
        # Test the homepage route for redirection
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  

    def test_show_users(self):
        # Test the show_users route
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)  


    # Add more test methods for different routes...

if __name__ == '__main__':
    unittest.main()

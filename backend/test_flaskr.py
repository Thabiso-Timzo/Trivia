import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("trivia", "trivia", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_categories_invalid(self):
        res = self.client().delete("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)

    def test_paginate_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])

    def test_get_paginate_bad_request(self):
        res = self.client().get("/questions?page=999")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

    
    def test_delete(self):
        res = self.client().delete("/questions/6")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_invalid(self):
        res = self.client().delete("/questions/10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Page not found")

    def test_post_question(self):
        new_question = {
            "question": "what is your name?'",
            "answer": "Thabiso",
            "difficulty": 5,
            "category": 5
        }
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_search(self):
        search = {"search": "What is", }
        res = self.client().post("/questions/search", json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 10)

    def test_search_invalid(self):
        search = {"search": 'what is .......'}
        res = self.client().post("/search", json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        #self.assertEqual(data['message'], 'Page not found')
    
    def test_questions_in_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertNotEqual(len(data["questions"]), 0)
        self.assertEqual(data["current_category"], "Science")
    
    def test_questions_in_category_invalid(self):
        res = self.client().get("/categories/100/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_quiz(self):
        input_data = {
            "previous_questions":[1, 3],
            "quiz_category": {
                "id": 5,
                "type": "Art"
            }
        }

        res = self.client().post("/quizzes", json=input_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

        self.assertNotEqual(data["question"]["id"], 1)
        self.assertNotEqual(data["question"]["id"], 3)

        self.assertEqual(data["question"]["category"], 5)

    # Its working
    def test_quiz_invalid(self):
        quiz = {
            'previous_questions': [6],
            'quiz_category': {
                'type': '2022',
                'id': '100000000'
            }
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
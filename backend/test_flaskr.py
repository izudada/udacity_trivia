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
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgresql://{}:{}@{}/{}".format('izudada', '1234567#','127.0.0.1:5432', self.database_name)
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

    def test_paginated_category_for_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertAlmostEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_questions_route_for_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertAlmostEqual(res.status_code, 200)
        self.assertEqual(data['currentCategory'], None)

    def test_a_category_of_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['currentCategory'])

    def test_delete_question_route(self):
        # Note the question id used in this test hsould 
        # be an existing question
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['message'])
        self.assertEquals(data['message'], "Question 5 was deleted successfully")

    def test_quizzes_route(self):
        res = self.client().post('/quizzes',  json={
            'previous_questions': [5, 12],
            'quiz_category': 4
        })
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(len(data), 1)

    def test_questions_add(self):
        res = self.client().post(
                                    '/questions',  
                                    json={
                                            'question': 'Heres a new question string',
                                            'answer': 'Heres a new answer string',
                                            'difficulty': 1,
                                            'category': 4
                                        }
                                )
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)

    def test_search_question(self):
        res = self.client().post('questions', json={
            'searchTerm': 'Question'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalQuestions'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

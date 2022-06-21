import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    def pagination(request, selection):
        """
            A pagination function that paginates questions when querried for
        """
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    
    def get_all_category():
        """
            A function that gets all the avialble category 
        """
        selection = Category.query.all()
        all_category = [category.format() for category in selection]

        return all_category

    
    def sort_questions(question_list, prev):
        """
            A function to sort a list of questions
        """
        result = [ 
            question.format() for question in question_list if question.id not in prev
        ]
        return result
       
    @app.route('/categories')
    def categories():
        """
            Create an endpoint to handle GET requests
            for all available categories.
        """
        try:
            all_categories = get_all_category()

            if len(all_categories) == 0:
                abort(404)

            return jsonify(
                {
                    "categories": all_categories
                }
            )
        except Exception as e:
            abort(400)

    @app.route('/questions', methods=['GET', 'POST'])
    def questions():
        """
            An endpoint to handle GET requests for questions,
            including pagination (every 10 questions);
            and also to create or post a new question
        """
        try:
            if request.method == 'GET':
                selection = Question.query.all()
                all_questions = pagination(request, selection)
                all_category = get_all_category()

                if len(all_questions) == 0:
                    abort(404) 

                return jsonify(
                    {
                        'questions': all_questions,
                        'totalQuestions': len(Question.query.all()),
                        'categories': all_category,
                        'currentCategory': None
                    }
                )
            else:
                body = request.get_json()
                question = body.get("question", None)
                answer = body.get("answer", None)
                difficulty = body.get("difficulty", None)
                category = body.get("category", None)

                if question and answer and difficulty and category:
                    question = Question(
                        question=question, answer=answer, difficulty=difficulty, category=category
                        )
                    question.insert()
                    return jsonify({
                        'success': True
                    })
                else:
                    abort(404)

        except Exception as e:
            abort(400)


    @app.route('/questions/<int:id>', methods=['DELETE'])
    def remove_question(id):
        """
            An endpoint to DELETE question using a question ID.
        """
        try:
            question = Question.query.get(id)

            if question == None:
                abort(404)
            else:
                question.delete()
                return jsonify(
                    {
                        "status": "sucess",
                        "message": f"Question {question.id} was deleted successfully"
                    }
                )
        except Exception as e:
            abort(400)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/categories/<int:id>/questions')
    def single_category(id):
        """
            A GET endpoint to get questions based on category.
        """
        try:
            category = Category.query.get(id)
            category_questions = Question.query.filter(Question.category==id).order_by(Question.id).all()
            questions = pagination(request, category_questions)

            return jsonify(
                {
                    'questions': questions,
                    'totalQuestions': len(questions),
                    'currentCategory': category.type
                }
            )

        except Exception as e:
            abort(400)

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        """
            An POST endpoint to get questions to play the quiz.
        """
        question = {}
        body = request.get_json()

        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)

        try:
            if quiz_category == None:
                selection = Question.query.all()
                all_questions = sort_questions(selection, previous_questions)
                question = random.choice(all_questions)
            else:
                questions = Question.query.filter(Question.category==quiz_category).order_by(Question.id).all()
                new_questions = sort_questions(questions, previous_questions)
                question = random.choice(new_questions)
            
            return jsonify(
                {
                    'question': question
                }
            )
        except Exception as e:
            abort(400)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable"
            }), 422


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad request"
            }), 400
    
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "Method not allowed"
            }), 405

    return app


# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## API Documentation
The API interacts with the trivia database, and helps users to retrieve questions or categories, create new questions, and go through a quiz-like gameplay scenario.

### Getting started
- Base URL: The API is currently only accessible via your localhost server and can be accessed locally via http://127.0.0.1:5000/ or localhost:5000
- Authentication: No authentication or API keys are required to access the API at this time.

### Error Handling
The Trivia API uses conventional HTTP response codes for successes and failures of API requests. As a reminder: Codes `2xx` indicate success, `4xx` indicate failures (such as a bad request or a request for non-existent data), and `5xx` indicate server errors (which means something went wrong with your local server).

Errors are parsed back to the user as JSON-encoded messages in the format below:

    {
            "success": False,
            "error": 404,
            "message": "resource not found"
    }

You can expect the following error codes when using the API:
+ `400 - Bad Request: The request wasn't accepted, often because of a missing parameter`
+ `404 - Not Found: The requested resource doesn't exist on the server`
+ `422 - Unprocessable: An error in your request is preventing the server from processing it`

### Endpoints

-    Documentation for this endpoints can be found [here](https://documenter.getpostman.com/view/20677030/UzBnrSnC)


## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

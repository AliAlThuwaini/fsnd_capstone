# Udacity Full Stack Developer Nanodegree Capstone Project

## Motivation

Create a back-end application which demonstrates the functinality of endpoints with Role Based Access tests.
To implement that JWT authentication has been included in the project and current JWT's has been provided for testing.
The motivation for this project is to demonstrate skills in combining the use of authorization tools, RBAC endpoints, error handling, test writing and handling data between the front and back-end of the application.

- Coding standards: PEP8 compliant code
- Authorization: RBAC roles and JWT is implemented by the 3rd party Auth0.
- Testing: Comprehensive RBAC and error handling has been implemented as part of the test-driven development process.
- Documentation: Setup instructions and endpoints has been documented.
- Deployment: The final code is deployed on Heroku and tests can be run agains its database.

This project is for a movie agency which has movies and actors listed in its database. There are three roles, Casting Assistant,  Casting Director & Executive Producer. For viewing the list of movies and actors in the database the user should be logged with the Casting Assistant role. To fully control actors (add, delete and modify) or modify movies the role of the user has to be Casting Director. However, to have full control over both actors and movies, Executive Producer role has to be in place.

## Setup and dependencies

This project is based on Python3, pip and psql. Please make sure these are pre-installed on your system.
To start the project create a virtual environment in the downloaded project folder with the following bash commands:

```bash
python3 -m venv env
source env/bin/activate
```

Following this install the required packages, PIP dependencies by running:

```bash
pip install -r requirements.txt
```

There are environment variables such as JWT codes and the database URL are stored in the setup.sh file.
Before running the test file execute:

```bash
source setup.sh
```

Following this the application endpoints are ready to be tested with the deployed server by running:

```bash
python test_app.py
```

The deployed application can be found here:

https://fsnd-capstone-ali.herokuapp.com/
git 

Note: If the existing JWT's are expired new ones could be obtained by following the link on the application homepage on auth0. The URL to the login can be generated from auth_url_generator.ipynb which can be found in auth folder.

assistant:          applicaitonsignin@gmail.com
director:           miningsavvy@gmail.com
executive producer: althuwaini.ali@gmail.com


You'll be redirected to the main page where the JWT can be copied from the URL after the # part.
in case you're using postman to call the endpoint, paste the JWT under the authorization tab and don't forget to use Bearer as auth type. For unittest, paste the each role's JWT to the repective variable in the beginning of the file (test_app.py)

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Avaible Endpoints

In order to play the game, a number of operations take place, each one of them belong to a specific endpoint. The available operations are:

- [/](#homePage)
- [GET movie](#getMovie)
- [GET actor](#getActor)
- [DELETE movie](#deleteMovie)
- [POST movie](#postMovie)
- [PATCH movie](#patchMovie)

---

<h4 id="homePage"></h4>

> '/'

This is the main page of the application, it displays a link to log in and generate new JWT tokens.

---

<h4 id="getMovie"></h4>

> **GET '/movie'**

This endpoint fetches all movies.

**Request Arguments:**

- _None_

**Returns:** The return should include an success: True message along with a list of movies in JSON format.

```javascript
{
  'success': True,
  'movies': movie_list_json
}
```

---

<h4 id="getActor"></h4>

> **GET '/actor'**

This endpoint fetches all actors.

**Request Arguments:**

- _None_

**Returns:** The return should include an success: True message along with a list of movies in JSON format.

```javascript
{
  'success': True,
  'actors': actor_list_json
}
```

---

<h4 id="deleteMovie"></h4>

> **DELETE '/movie/<int:movie_id>'**

This endpoint allows you to delete a movie, based on its id.

**Request Arguments:**

- _movie_id_ (integer) of the movie to delete.

**Returns:** An object with a success message, the id of the movie deleted and the new amount of questions avaibale.

```javascript
{
  'success': True,
  'movie_id': movie_id
}
```

---

<h4 id="postMovie"></h4>

> **POST '/add-movie'**

This endpoint allows you to POST a movie.

**Request Arguments:**

A JSON object containing the title and the release date:

```javascript
{
  'title': 'title',
  'release_date': 'release_date'
}
```

**Returns:** If there are no errors the same JSON data will be returned:

```javascript
{
  'title': 'title',
  'release_date': 'release_date'
}
```

---

<h4 id="patchMovie"></h4>

> **PATCH '/movie/<int:movie_id>'**

This endpoint allows you to PATCH an existing movie.

**Request Arguments:**

- _movie_id_ (integer) of the movie to be modified.

**Returns:** An object with a success message, and the patched movie in JSON format.

```javascript
{
  'success': True,
  'movie': patched_movie_json
}
```

---

## Testing

To run the tests, run

```
python test_app.py
```

# Available Roles

There are 3 roles and 8 different permissions defined in the Authorization backend for this application

## Permissions:

    ```
    'get:movie': Get the list of all movies
    'get:actor': Get the list of all actors
    'post:movie': Post a new movie
    'post:actor': Post a new actor
    'delete:movie': Delete an exsiting movie
    'delete:actor': Delete an exsiting actor
    'patch:movie': Modify an exsiting movie
    'patch:actor': Modify an exsiting actor
    ```

## Roles

### Casting Assistant

Can list actors and movies.

### Casting Director

Can list movies, actors, post movies, modify movies and delete movies.

### Executive Director

Can list (movies, actors), post (movies, actors), modify (movies, actors) and finally (delete movies, actors).

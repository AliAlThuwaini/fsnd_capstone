#import os
#from castagency.models import Movies
from flask import Flask, request, abort, jsonify
#from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from auth import AuthError, requires_auth




#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  #app.url_map.strict_slashes = False
  setup_db(app)

  # CORS app
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers',
      'Content-Type,Authorization,true')
    response.headers.add(
      'Access-Control-Allow-Methods',
      'GET, DELETE, POST, PATCH, OPTIONS')
    return response



  #----------------------------------------------------------------------------#
  # Controllers
  #----------------------------------------------------------------------------#

  # This is a general home just to make sure things are working
  @app.route('/', methods=['GET'])
  def home_page():
    movies = Movies.query.all()
    return jsonify({
      'success': True,
      'message': 'It worked',
      'code': 200 ,
      'movie_titles': {movie.id: movie.title for movie in movies},
      })

  #============================
  # Movies:
  #============================

  # Get Movies
  @app.route('/movie', methods=['GET'])
  @requires_auth('get:movie')
  def get_movies(payload):
    movies = Movies.query.all()
    if (len(movies) == 0):
      abort(404)
    try:
      return jsonify({
        'success': True,
        'movies': {movie.id: movie.title for movie in movies}
        })

    except:
      abort(422)


  # @app.route('/add-movi', methods=['POST'])
  # def add_movi():
  #   data = request.get_json()
  #   try:
  #     # Ensure that all required fields to create a movie are supplied
  #     title = data.get('title', None)
  #     release_date = data.get('release_date', None)
  #     print ('Movie title: ', title, '\n', 'Movie release date: ', release_date)

  #   except Exception as error:
  #     print(f"\nerror => {error}\n")
  #     abort(422)

  #   return jsonify({
  #     'title': title,
  #     'release_date': release_date
  #   })



  # Add new movie
  @app.route('/add-movie', methods=['POST'])
  @requires_auth('post:add-movie')
  def add_movie(payload):
    data = request.get_json() 

    try:
      # Ensure that all required fields to create a movie are supplied
      title = data.get('title', None)
      release_date = data.get('release_date', None)
      
      if ((title is None) or (release_date is None)):
        abort(422)

      else:
        # Create the movie instance
        movie = Movies(title=title, release_date=release_date)

        # insert the new movie into db
        movie.insert()
        
        return jsonify({
          'success': True,
          'message': f'Movie with title "{title}" is inserted into DB',
          'movie': movie.format()
          })

    except Exception as error:
      print(f"\nerror => {error}\n")
      abort(422)



  # Edit an existing movie:
  @app.route('/movie/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  #@requires_auth('patch:movie')
  def update_movie(payload, movie_id):

    data = request.get_json()
    # extract that specific movie to be updated from the db
    movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
    
    # if movie not found, exit with 404
    if not movie:
        abort(404)
    
    try:
      # Ensure that all required fields to create a movie are supplied
      if 'title' in data:
            movie.title = data['title']
      if 'release_date' in data:
          movie.release_date = data['release_date']

      movie.update()

      return jsonify({
          'success': True,
          'movie': movie.format(),
      }), 200

    except Exception as error:
      print(f"\nerror => {error}\n")
      abort(500)


  # Delete an existing movie:
  @app.route('/movie/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  #@requires_auth('delete:movie')
  def delete_movie(payload, movie_id):
    if not movie_id:
        abort(404)

    # Get the movie to be deleted
    to_delete_movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
    if not to_delete_movie:
        abort(404)
    # delete the movie
    to_delete_movie.delete()

    return jsonify({
        'success': True,
        'movie_id': movie_id
    }), 200





  #============================
  # actors:
  #============================

  # Get actors
  @app.route('/actor', methods=['GET'])
  @requires_auth('get:actor')
  def get_actors(payload):
    actors = Actors.query.all()
    if (len(actors) == 0):
      abort(404)
    try:
      return jsonify({
        'success': True,
        'actors': {actor.id: actor.name for actor in actors}
        })
    except:
      abort(422)



  # Add new actor
  @app.route('/add-actor', methods=['POST'])
  @requires_auth('post:add-actor')
  #@requires_auth('post:actors')
  def add_actor(payload):
    data = request.get_json()

    try:
      # Ensure that all required fields to create a actor are supplied
      name = data.get('name', None)
      age = data.get('age', None)
      gender = data.get('gender', None)
      
      if ((name is None) or (age is None) or (gender is None) ):
        abort(422)

      else:
        # Create the actor instance
        actor = Actors(name=name, age=age, gender=gender)

        # insert the new actor into db
        actor.insert()

        return jsonify({
          'success': True,
          'message': f'Actor with name "{name}" is inserted into DB',
          'actor': actor.format()
          })

    except Exception as error:
      print(f"\nerror => {error}\n")
      abort(422)


  # Edit an existing actor:
  @app.route('/actor/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actor')
  #@requires_auth('patch:actor')
  def update_actor(payload, actor_id):

    data = request.get_json()
    # extract that specific actor to be updated from the db
    actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
    
    # if actor not found, exit with 404
    if not actor:
        abort(404)
    
    try:
      # Ensure that all required fields to create a actor are supplied
      if 'name' in data:
            actor.name = data['name']
      if 'age' in data:
          actor.age = data['age']
      if 'gender' in data:
          actor.gender = data['gender']

      actor.update()

      return jsonify({
          'success': True,
          'actor': actor.format(),
      }), 200

    except Exception as error:
      print(f"\nerror => {error}\n")
      abort(500)


  # Delete an existing actor:
  @app.route('/actor/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  #@requires_auth('delete:actor')
  def delete_actor(payload, actor_id):
    if not actor_id:
        abort(404)

    # Get the actor to be deleted
    to_delete_actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
    if not to_delete_actor:
        abort(404)
    # delete the actor
    to_delete_actor.delete()

    return jsonify({
        'success': True,
        'actor_id': actor_id
    }), 200


  #----------------------------------------------------------------------------#
  # Error Handling
  #----------------------------------------------------------------------------#

  '''
  Example error handling for unprocessable entity
  '''
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422



  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request. Check request body"
      }), 400


  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404


  @app.errorhandler(401)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 401,
          "message": "Authorization Header missing, expected but not found!!"
      }), 401

  
  @app.errorhandler(403)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 403,
          "message": "User is not unauthorized to perform the process!!"
      }), 403


  @app.errorhandler(AuthError)
  def authError(error):
      return jsonify({
          "success": False,
          "error": error.status_code,
          # "message": error.error['description']
          "message": error.error
      }), error.status_code


#Ali: consider adding error 405


  return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)



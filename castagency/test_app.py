# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import json
import os
import unittest
#from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies



# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------


class AgencyTestCase(unittest.TestCase):
    """This class represents the casting agency's test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('student', 'student','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass



    # *************************************************
    # Movies Tests
    # *************************************************

    # ********************
    # Get movies
    # ********************

    def test_get_all_movies(self):
        # Insert dummy movie into database.
        movies = Movies(title="test_get_all_movies", release_date="2021-03-01T21:30:00.000Z")
        movies.insert()

        res = self.client().get('/movie')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        movies = Movies.query.all()
        self.assertEqual(len(data['movies']), len(movies))


    def test_get_movies_method_dont_accept_post_request(self):
        res = self.client().post('/movie')
        self.assertEqual(res.status_code, 405)


    # ********************
    # Post movies
    # ********************

    def test_successful_create_new_movie(self):
        new_movie = {
            'title': "test_successful_create_new_movie",
            'release_date': "2021-03-01T21:30:00.000Z"
        }

    
        res = self.client().post('/add-movie', json=new_movie)
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        movie_added = Movies.query.get(data['movie']['id'])
        self.assertTrue(movie_added)



    def test_422_missing_date_movie_not_allowed(self):
        new_movie = {
          'title': "test_422_missing_date_movie_not_allowed",
          }

        res = self.client().post('/add-movie', json=new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertFalse(data['success'])


    # ********************
    # PATCH movies
    # ********************

    def test_successful_update_existing_movie_data(self):
        # instert dummy movie
        movie = Movies(title="test_successful_update_existing_movie_data", release_date="2024-03-01T21:30:00.000Z")
        movie.insert()

        movie_patch = {
            'release_date': '2060-03-01T21:30:00.000Z'
        } 

        res = self.client().patch(f'/movie/{movie.id}', json=movie_patch)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], movie.title)
        self.assertEqual(data['movie']['release_date'], "Mon, 01 Mar 2060 21:30:00 GMT")

        updated_movie = Movies.query.filter(Movies.id == data['movie']['id']).one_or_none()
        self.assertEqual(updated_movie.id, movie.id)

    # fail to update non existing movie
    def test_404_update_nonexisting_movie(self):
        movie_patch = {
          'title': "Fake Movie"
        } 

        res = self.client().patch(f'/movie/1000', json=movie_patch)
        # print('type of response: ', type(res))
        # print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])


    # ********************
    # DELETE movies
    # ********************

    def test_successful_delete_existing_movie(self):
        movie = Movies(title="Movie to delete", release_date="'2025-03-01T21:30:00.000Z")
        movie.insert()

        res = self.client().delete(f'/movie/{movie.id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_id'], movie.id)


    def test_404_delete_nonexisting_movie(self):
        res = self.client().delete('/movie/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])




    # *************************************************
    # Actors Tests
    # *************************************************

    # ********************
    # GET Actors
    # ********************

    def test_should_return_all_actors(self):
        # Insert dummy actor into database.
        actor = Actors(name="Fake Actor", age="30", gender="male")
        actor.insert()

        res = self.client().get('/actor')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actors = Actors.query.all()
        self.assertEqual(len(data['actors']), len(actors))


    def test_get_actors_doesnt_accept_post_request(self):
        res = self.client().post('/actor')
        self.assertEqual(res.status_code, 405)


    # ********************
    # POST Actors
    # ********************

    def test_successful_create_new_actor(self):
        new_actor= {
            'name': "New actor to post",
            'age': 50,
            'gender': "female"
        } 

        res = self.client().post('/add-actor', json= new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], new_actor['name'])
        self.assertEqual(data['actor']['age'], new_actor['age'])
        self.assertEqual(data['actor']['gender'], new_actor['gender'])
        # make sure the new actor is in the db
        self.assertTrue(Actors.query.get(data['actor']['id']))


    def test_422_missing_age_actor_not_allowed(self):
        new_actor= {
            'name': "New actor with missing age",
            'gender': "male"
        } 

        res = self.client().post('/add-actor', json= new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertFalse(data['success'])


    # ********************
    # PATCH Actors
    # ********************

    def test_successful_update_existing_actor(self):
        actor = Actors(name="New actor to patch", age=40, gender="female")
        actor.insert()

        actor_data_patch = {
            'age': 20
        } 

        res = self.client().patch(f'/actor/{actor.id}', json= actor_data_patch)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor.name)
        self.assertEqual(data['actor']['age'], actor_data_patch['age'])
        self.assertEqual(data['actor']['gender'], actor.gender)

        actor_updated = Actors.query.get(data['actor']['id'])
        self.assertEqual(actor_updated.id, actor.id)


    def test_404_update_nonexisting_actor(self):
        actor_data = {
            'age': 1
        } 

        res = self.client().patch('/actors/10000', json=actor_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])


    # ********************
    # DELETE Actors
    # ********************

    def test_successful_delete_existing_actor(self):
        actor = Actors(name="Actor to be deleted", age="37", gender="female")
        actor.insert()

        res = self.client().delete(f'/actor/{actor.id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], actor.id)


    def test_404_delete_nonexisting_actor(self):

        res = self.client().delete('/actor/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


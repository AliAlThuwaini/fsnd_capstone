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
# Authorization info
# ---------------------------------------------------------

#res = self.client().post(f"/movie", data=json.dumps(self.test_movie), content_type='application/json', headers=self.director_headers)

#res = self.client().get(f"/movie", content_type='application/json', headers=self.assistant_headers)


assistant_auth = {
  "Content-Type": "application/json",
  "Authorization": "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtRbGxWQk1iVEZPbVJOMDV5ellzRCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWxpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDNlODQwODU2OTI0MzAwNzBjMGViYWIiLCJhdWQiOiJjYXN0aW5nX2FnZW5jeSIsImlhdCI6MTYxNDc4NjU0MSwiZXhwIjoxNjE0ODcyOTQxLCJhenAiOiIyYmdtSUdiVnc0NnpWRzdWRTBEQVZveG5yM3ZzWHpQOCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIl19.YNzZ48QRs_imrXYj7yi883YyyPoqCVlmwrIj5BgkfZ_ruwhWmVeHSpKNVoz2psOTPUdOwAT3UpINwOjRGOV6qEtX5DLNlDShh3qb9GjfVSyD07sLOJvuhGLstLW9BVyilVPESfqFu3qsQQ8knuL_-ZnEmsc6ZcEvSU1Rdr-ONAWyYp4zwIsMl-gKkAJu2PfICesMGBPlWMvOS7Tg5WL6W1ol0bvABUZF6SuIASxs-fJb6kOCDhk8mm5y4Q4U0og2a4-a5EedXPslWRXeVVQgiV1q_rJhqa9gNE3zqW8B3jO7RWek1MstiM8SqPDjd8rdYIIlsQCms69SiMuZKGbJWA"
}

director_auth = {
  "Content-Type": "application/json",
  "Authorization": "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtRbGxWQk1iVEZPbVJOMDV5ellzRCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWxpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDFjMTM2YzRjMzBmNzAwNmE3ZDU2NzIiLCJhdWQiOiJjYXN0aW5nX2FnZW5jeSIsImlhdCI6MTYxNDc4NjY4MiwiZXhwIjoxNjE0ODczMDgyLCJhenAiOiIyYmdtSUdiVnc0NnpWRzdWRTBEQVZveG5yM3ZzWHpQOCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWRkLWFjdG9yIl19.CeMiJsXls4K-2AAcvo8LHNtsW2ZhQwZQ0KbAtrFoYADn1d5gAEnLcVSUP8J8ynMQRRUNj4UxGa5PrMAIXYOOuxCWj8zBDdgtjvq1mNX6f6gdupvtr17PYEz33Li4R6orx0N8QOyvHlxCHg6uJyBxHRhTdHuRNtC1mL4eslnYejOouKRnBl52ip_-KrmYtP-QYYBkGUK9XgO8u2WayeWi9lEM28xRBLimuk5BaM2xi2wnt0VEOEmkEgzPwAYM6rC8PgU1t4DXujrYl8Gf4P-JmzknzpFC9o1t1i7CKi9SVht7gGmVSyTXf1UJeRWPHmi-ee6Yc7-TtFE4ZQD4uFfnsA"
}

exec_producer_auth = {
  "Content-Type": "application/json",
  "Authorization": "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtRbGxWQk1iVEZPbVJOMDV5ellzRCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWxpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDFjMTJkNjU0YzFkNzAwNzFlY2ZjODUiLCJhdWQiOiJjYXN0aW5nX2FnZW5jeSIsImlhdCI6MTYxNDc4Njc5MywiZXhwIjoxNjE0ODczMTkzLCJhenAiOiIyYmdtSUdiVnc0NnpWRzdWRTBEQVZveG5yM3ZzWHpQOCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWRkLWFjdG9yIiwicG9zdDphZGQtbW92aWUiXX0.tTnyz4k_eBx-d4q2NdaQSnp5NIZ2eDtfiHYkK82fHnBaNAyjnZzjM29lfMq8wpiQE07gpsQz6nqqcfNhCEHoBCp1TGI2iPYXueMKue7qQTZS9_Ww5z-NbyCK0TjDjvVKBMBmF7eHtOO-FzKv23-bGli6Q3rWPan6et7A7Tb_POMFXMmFZ49N0j5JjOEdb0J7s_rJ5jNhFaH714sr-TTDno1zLFrWDtQH3Cacmwpuk5VDWsOMZHMFD6JinnUkGAsvAjQgz_lA_OtrChUL8q698E7bkphyVpDAwMfa-mjBPEvSx7JQAwiKrugM6ml4S5Mku3tIi3uz8InDlyVij_rtUQ"
}




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

        #res = self.client().get('/movie')
        res = self.client().get(f"/movie", content_type= assistant_auth['Content-Type'], headers= assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        movies = Movies.query.all()
        self.assertEqual(len(data['movies']), len(movies))


    def test_get_movies_method_dont_accept_post_request(self):
        res = self.client().post('/movie')
        self.assertEqual(res.status_code, 405)


    #********************
    #Post movies
    #********************

    def test_successful_create_new_movie(self):
        new_movie = {
            "title": "test_successful_create_new_movie",
            "release_date": "2021-03-01T21:30:00.000Z"
        }

        res = self.client().post(f"/add-movie", data=json.dumps(new_movie), content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        movie_added = Movies.query.get(data['movie']['id'])
        self.assertTrue(movie_added)



    def test_422_missing_date_movie_not_allowed(self):
        new_movie = {
          'title': "test_422_missing_date_movie_not_allowed",
          }

        res = self.client().post(f"/add-movie", data=json.dumps(new_movie), content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
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

        #res = self.client().patch(f'/movie/{movie.id}', json=movie_patch)
        res = self.client().patch(f"/movie/{movie.id}", data=json.dumps(movie_patch), content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
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

        #res = self.client().patch(f'/movie/1000', json=movie_patch)
        res = self.client().patch(f"/movie/1000", data=json.dumps(movie_patch), content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
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

        #res = self.client().delete(f'/movie/{movie.id}')
        res = self.client().delete(f"/movie/{movie.id}", content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_id'], movie.id)


    def test_404_delete_nonexisting_movie(self):
        #res = self.client().delete('/movie/10000')
        res = self.client().delete(f"/movie/1000", content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
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

        #res = self.client().get('/actor')
        res = self.client().get(f"/actor", content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actors = Actors.query.all()
        self.assertEqual(len(data['actors']), len(actors))


    def test_get_actors_doesnt_accept_post_request(self):
        #res = self.client().post('/actor')
        res = self.client().post(f"/actor", content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
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

        #res = self.client().post('/add-actor', json= new_actor)
        res = self.client().post(f"/add-actor", data = json.dumps(new_actor), content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
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

        #res = self.client().post('/add-actor', json= new_actor)
        res = self.client().post(f"/add-actor", data = json.dumps(new_actor), content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
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

        #res = self.client().patch(f'/actor/{actor.id}', json= actor_data_patch)
        res = self.client().patch(f"/actor/{actor.id}", data = json.dumps(actor_data_patch), content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
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

        #res = self.client().patch('/actor/10000', json=actor_data)
        res = self.client().patch(f"/actor/10000", data= json.dumps(actor_data), content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
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

        #res = self.client().delete(f'/actor/{actor.id}')
        res = self.client().delete(f"/actor/{actor.id}", content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], actor.id)


    def test_404_delete_nonexisting_actor(self):

        res = self.client().delete('/actor/10000')
        res = self.client().delete(f"/actor/1000", content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])



    #*************************************************
    #            Authenication Tests
    #*************************************************


    # ********************
    # Assistant Role
    # ********************

    def test_assistant_successful_return_all_actors(self):
        # Insert dummy actor into database.
        actor = Actors(name="Fake Actor", age="30", gender="male")
        actor.insert()

        #res = self.client().get('/actor')
        res = self.client().get(f"/actor", content_type=assistant_auth['Content-Type'], headers= assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actors = Actors.query.all()
        self.assertEqual(len(data['actors']), len(actors))


    def test_assistant_fail_to_update_existing_actor(self):
      actor = Actors(name="New actor to patch", age=40, gender="female")
      actor.insert()

      actor_data_patch = {
          'age': 20
      } 

      #res = self.client().patch(f'/actor/{actor.id}', json= actor_data_patch)
      res = self.client().patch(f"/actor/{actor.id}", data = json.dumps(actor_data_patch), content_type=assistant_auth['Content-Type'], headers= assistant_auth)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 403)
      self.assertFalse(data['success'])


    # ********************
    # Director Role
    # ********************


    def test_director_successful_return_all_actors(self):
        # Insert dummy actor into database.
        actor = Actors(name="Fake Actor", age="30", gender="male")
        actor.insert()

        #res = self.client().get('/actor')
        res = self.client().get(f"/actor", content_type=director_auth['Content-Type'], headers= director_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actors = Actors.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    
    def test_director_fail_to_delete_existing_movie(self):

        movie = Movies(title="Movie to delete", release_date="'2025-03-01T21:30:00.000Z")
        movie.insert()

        #res = self.client().delete(f'/movie/{movie.id}')
        res = self.client().delete(f"/movie/{movie.id}", content_type=director_auth['Content-Type'], headers= director_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])


    # *************************
    # Executive Producer Role
    # *************************

    #This is a repetion test to the above functions. However, the intend here is to show how the role is funcitoning against its supposed authrization

    def test_exec_prod_successful_delete_existing_actor(self):
      actor = Actors(name="Actor to be deleted", age="37", gender="female")
      actor.insert()

      #res = self.client().delete(f'/actor/{actor.id}')
      res = self.client().delete(f"/actor/{actor.id}", content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertTrue(data['success'])
      self.assertEqual(data['actor_id'], actor.id)



    def test_exec_prod_successful_delete_existing_movie(self):
        movie = Movies(title="Movie to delete", release_date="'2025-03-01T21:30:00.000Z")
        movie.insert()

        #res = self.client().delete(f'/movie/{movie.id}')
        res = self.client().delete(f"/movie/{movie.id}", content_type=exec_producer_auth['Content-Type'], headers= exec_producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_id'], movie.id)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


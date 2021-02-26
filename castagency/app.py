import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS




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


    

  return app



APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)



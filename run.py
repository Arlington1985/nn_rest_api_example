#!/usr/bin/env python
import os
from flask import Flask
from flask_restful import Api
from app.config import app_config
from app.resources import OperationList, OperationResource, UserResource, UploadResource
from app.db import db

# This will load app/__init__.py file which Flask will load Flask
from app import app


# Initializing Flask-RESTful
api = Api(app)

# Bound database
db.init_app(app)

# Declaring Resources of REST API
api.add_resource(OperationList, '/operations/all', endpoint='operations')
api.add_resource(OperationResource, '/operations', endpoint='operation_new')
api.add_resource(OperationResource, '/operations/<string:id>', endpoint='operation')
api.add_resource(UserResource, '/users', endpoint='users')
api.add_resource(UserResource, '/users/<string:id>', endpoint='user')
api.add_resource(UploadResource, '/'+app.config['UPLOAD_FOLDER']+'/<string:filename>', endpoint='files')

# Calling main
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])

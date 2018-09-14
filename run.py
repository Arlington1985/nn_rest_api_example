#!/usr/bin/env python
import os
#from flask import Flask
from flask_restful import Api
from config import app_config
from app.resources import MainPage, OperationList, OperationId, MyUser, UserId, UploadFile
from app.db import db

# This will load app/__init__.py file which Flask will load Flask
from app import app


# Initializing Flask-RESTful
api = Api(app, catch_all_404s=True)

# Bound database
db.init_app(app)

# Declaring Resources of REST API
api.add_resource(MainPage, '/', endpoint='main')
api.add_resource(OperationList, '/operations', endpoint='operationlist')
api.add_resource(OperationId, '/operations/<int:id>', endpoint='operationid')
api.add_resource(MyUser, '/user', endpoint='myuser')
api.add_resource(UserId, '/user/<int:id>', endpoint='userid')
api.add_resource(UploadFile, '/'+app.config['UPLOAD_FOLDER']+'/<string:filename>', endpoint='files')

# Calling main
if __name__ == '__main__':
    print(app.config['APP_URL'])
    app.run(debug=app.config['DEBUG'], host=app.config['APP_URL'],port=os.getenv('PORT'))

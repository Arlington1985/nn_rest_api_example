#Global configuration 

import os

class Config(object):
    # Parent configuration class.
    BASEDIR = os.getcwd()
    UPLOAD_FOLDER = 'uploads'
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    APP_URL = "0.0.0.0"
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    # Business config
    ALLOWED_EXTENSIONS = set(['txt'])
    TRADEMARK_SYMBOL='®'



class DevelopmentConfig(Config):
    # Development configuration class
    DEBUG = True
    


class TestingConfig(Config):
    # Development configuration class, with a seperate database
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEBUG = True


class ProductionConfig(Config):
    # Production configuration class
    DEBUG = False
    TESTING = False
    #APP_URL = "nn-rest-api.herokuapp.com"


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
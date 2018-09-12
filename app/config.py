#Global configuration 

import os

class Config(object):
    # Parent configuration class.
    BASEDIR = os.getcwd()
    UPLOAD_FOLDER = 'uploads'
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = "sqlite://"+os.path.join(BASEDIR,os.getenv('DATABASE_URL').split("///")[-1])
    APP_URL = "http://localhost:5000"
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
    APP_URL = "Heroku url"


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
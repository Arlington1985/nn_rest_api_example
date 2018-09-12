# Initializing Flask and loading configuration 
# from config file and environment variables

import os
from flask import Flask
from config import app_config


app = Flask(__name__, instance_relative_config=False)

config_name = os.getenv('FLASK_ENV') 
app.config.from_object(app_config[config_name])
print(app.config)
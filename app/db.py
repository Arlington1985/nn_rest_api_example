#Loading Database session

from app import app
from flask_sqlalchemy import SQLAlchemy

# first method
db = SQLAlchemy()

# second method
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(app.config['SQLALCHEMY_DATABASE_URI']))
session = scoped_session(Session)
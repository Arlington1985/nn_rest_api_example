#!/usr/bin/env python

# Manager for maintenance works
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.db import db
from app import app
from app.models import UserModel, OperationModel

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# Creating upload folder
@manager.command
def create_folder():
    print(app.root_path)
    print(app.instance_path)
    print(app.config['BASEDIR'])
    final_directory = os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER'])
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
        return "Folder with the name {} was created".format(final_directory)
    else:
        return "Folder with the name {} already exists".format(final_directory)

# Recreating database objects
@manager.command
def recreate_database():
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    print (app.config['SQLALCHEMY_DATABASE_URI'])
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return "Database recreated successfully"


if __name__ == '__main__':
    manager.run()
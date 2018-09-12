# Database schema model

from app import app
from app.db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, user, password):
        self.user = user
        self.password = password

    def get(id):
        user = session.query(UserModel).filter(UserModel.id == id).first()
        return user
    
    @classmethod
    def get_by_user(cls, user):
        user = cls.query.filter_by(user = user).first()
        return user


    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}    
#    def __repr__(self):
#        return self.name


class OperationModel(db.Model):
    __tablename__ = 'operations'

    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column( db.String(255) )
    original_file = db.Column( db.String(255) )
    keyword = db.Column( db.String(255) )
    generated_file = db.Column( db.String(255) )
    replace_count = db.Column( db.Integer )
    operation_timestamp = db.Column( db.DateTime, default=db.func.current_timestamp() )
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))

    def __init__(self, original_filename, original_file, keyword, generated_file, replace_count,  user_id):
        self.original_filename = original_filename
        self.original_file = original_file
        self.keyword = keyword
        self.generated_file = generated_file
        self.replace_count = replace_count
        self.user_id = user_id
    
    def get(id):
        operation = session.query(OperationModel).filter(OperationModel.id == id).first()
        return operation

    def get(user_id):
        return session.query(OperationModel).filter(OperationModel.user_id == user_id)

    def get(id, user_id):
        operation = session.query(OperationModel).filter(OperationModel.id == id, OperationModel.user_id == user_id).first()
        return operation


    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

#    def __repr__(self):
#        return "<Operations: {}>".format(self.original_file)


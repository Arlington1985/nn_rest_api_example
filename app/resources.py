# Main application logic is here
import os, uuid
from flask import Flask,  request, send_from_directory, url_for, make_response, jsonify, abort
from flask_restful import Resource, reqparse, marshal_with, abort, fields
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import or_
from werkzeug.utils import secure_filename
import werkzeug
from werkzeug.exceptions import HTTPException
from app.models import OperationModel, UserModel

# Loading here app because of reading config parameters and error handlers
from app import app

# Loading database 
from app.db import db, session


# Loading config parameters to local variables
UPLOAD_FOLDER=app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS=app.config['ALLOWED_EXTENSIONS']
APP_URL=app.config['APP_URL']
TRADEMARK_SYMBOL=app.config['TRADEMARK_SYMBOL']
BASEDIR=app.config['BASEDIR']



# Loading module for basic auth
auth = HTTPBasicAuth()


# Marshals for defining which fields will be visible in the response
operation_fields = {
    'id': fields.Integer,
    'original_filename': fields.String,
    'original_file': fields.String,
    'keyword': fields.String,
    'generated_file': fields.String,
    'replace_count': fields.Integer,
    'operation_timestamp': fields.DateTime,
}

user_fields = {
    'id': fields.Integer,
    'user': fields.String,
    'password':fields.String
}


class ConfilictHandler(HTTPException):
    code = 424
    description = 'Related records in operations'

werkzeug.exceptions.default_exceptions[424]=ConfilictHandler

# Handling if credentials were not provided in the header
@auth.verify_password
def verify_password(username, password):
    user = UserModel.query.filter_by(user = username, password = password).first()
    if user is None:
        abort(401, status="fail", message="Inavlid credentials in header")
    else:
        return True


# Function for checking allowed file extension
def allowed_file(filename):
   return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



parser = reqparse.RequestParser()
parser.add_argument('file', type=werkzeug.FileStorage, location='files')
parser.add_argument('keyword', type=werkzeug.FileStorage, location='files')

# if specified Delete related files of while removing operation
parser.add_argument('delete_files')


class OperationResource(Resource):
    
    # Operation detail
    @auth.login_required
    @marshal_with(operation_fields)
    def get(self, id):
        user=session.query(UserModel).filter(UserModel.user == request.authorization.username).first()
        operation = session.query(OperationModel).filter(OperationModel.id == id, OperationModel.user_id == user.id).first()
        if not operation:
            abort(404, status="fail", message="No such operation")
        return operation, 200

        
    # Adding new operation ( Replacing content with adding Trademark symbol)
    @auth.login_required
    @marshal_with(operation_fields)
    def post(self):
        parsed_args = parser.parse_args()        
        original_file=parsed_args['file']
        keyword=parsed_args['keyword']

        # check if the post request has the file and keyword part and they are not empty and they are allowed
        if original_file is None or keyword is None or not allowed_file(original_file.filename) or not allowed_file(keyword.filename):
            
            # init array for collecting responses
            response=[]

            # Check if file is specified
            if original_file is None:
                response.append("File parameter has not been specified: Type->File")

            # check if keyword is specified
            if keyword is None:
                response.append("Keyword parameter has not been specified: Type->File")

            # check if selected files are in allowed list
            if not allowed_file(original_file.filename) or not allowed_file(keyword.filename):
                response.append("Uploading files only in {} format is allowed".format(ALLOWED_EXTENSIONS))

            abort(400, status="fail", message=response)
        
        # Starting of part adding trademark symbol
        if original_file and keyword:
            
            # Security check of file name
            original_filename = secure_filename(original_file.filename)
            extension = os.path.splitext(original_filename)[1]

            # Coverting files to string
            keyword_text = keyword.read().decode("utf-8")
            text=original_file.read().decode("utf-8")

            # Generating uniq id for saving files safely without overlaping
            uniq_id=str(uuid.uuid4())

            # Saving original file to upload folder with new unique name
            original_file_n="original-"+uniq_id+extension
            with open(os.path.join(UPLOAD_FOLDER, original_file_n), "w") as f:
                f.write(text) 

            # Saving keyword file to upload folder with new unique name
            keyword_n="keyword-"+uniq_id+extension
            with open(os.path.join(UPLOAD_FOLDER, keyword_n), "w") as f:
                f.write(keyword_text) 

            # Counter for replacement
            count=0

            # Looping keywords key against words of original files
            for key in keyword_text.splitlines():
                while key in text.split():
                    
                    # with that logic also covered preventing adding trademark symbol
                    #   if already exist
                    # Adding trademark symbol to the end of the word
                    text=text.replace(key,key+TRADEMARK_SYMBOL,1)

                    # increasing replacement counter
                    count+=1


            #Saving generated file to upload folder with new unique name
            generated_file_n = "generated-"+uniq_id+extension
            with open(os.path.join(UPLOAD_FOLDER, generated_file_n), "w") as f:
                f.write(text)                

            # Fetching session user 
            user = session.query(UserModel).filter(UserModel.user == request.authorization.username).first()
            
            # Saving as a new operation to database
            operation = OperationModel(original_filename, os.path.join(APP_URL, UPLOAD_FOLDER, original_file_n), os.path.join(APP_URL, UPLOAD_FOLDER, keyword_n), os.path.join(APP_URL, UPLOAD_FOLDER, generated_file_n), count, user.id)
            OperationModel.add(operation)
            return operation, 201

    # Delete operation by operation id
    @auth.login_required
    @marshal_with(operation_fields)
    def delete(self, id):
        
        parsed_args = parser.parse_args()        
        delete_files=parsed_args['delete_files']
        user = session.query(UserModel).filter(UserModel.user == request.authorization.username).first()
        operation = session.query(OperationModel).filter(OperationModel.id == id, OperationModel.user_id ==user.id).first()


        # checking if requested operation exists
        if not operation:
            abort(404, status="fail", message="No such operation")

        # Deleting operation

        # Deleting related files if specified
        
        # Getting current session, it's not possible to delete row 
        # in SQLite while it's running on another session
        curr_sess=db.session.object_session(operation)
        curr_sess.delete(operation)
        del_count=0
        
        full_original=os.path.join(BASEDIR, UPLOAD_FOLDER, operation.original_file.split("/")[-1])
        if not os.path.exists(full_original) or os.remove(full_original):
            del_count+=1

        full_keyword=os.path.join(BASEDIR, UPLOAD_FOLDER, operation.keyword.split("/")[-1])
        if not os.path.exists(full_keyword) or os.remove(full_keyword):
            del_count+=1

        full_generated=os.path.join(BASEDIR, UPLOAD_FOLDER, operation.generated_file.split("/")[-1])
        if not os.path.exists(full_generated) or os.remove(full_generated):
            del_count+=1
            
        if del_count == 3:
            curr_sess.commit()
        else:
            curr_sess.rollback()
            abort(501, status="error", message="Cannot delete one of the related file, delete was not performed")


        return operation, 204

# Listing operations
class OperationList(Resource):
    @auth.login_required
    @marshal_with(operation_fields)
    def get(self):
        user = session.query(UserModel).filter(UserModel.user == request.authorization.username).first()
        operations = session.query(OperationModel).filter(OperationModel.user_id == user.id).all()
        
        # Checking if fetched operations list empty
        if not operations:
            return operations, 204

        return operations, 200


parser.add_argument('user')
parser.add_argument('password')


class UserResource(Resource):
    
    # User detail
    @auth.login_required
    @marshal_with(user_fields)
    def get(self):
        user=session.query(UserModel).filter(UserModel.user == request.authorization.username).first()
        if not user:
            abort(404, status="fail", message="No such user")
        return user
    
    # New user
    @marshal_with(user_fields)
    def post(self):
        parsed_args = parser.parse_args()        
        user=parsed_args['user']
        password=parsed_args['password']
        if session.query(UserModel).filter(UserModel.user == user).first():
            abort(409, status="fail", message="Username is taken")
        
        user=UserModel(user, password)
        UserModel.add(user)
        return user, 201


    # Delete curren logged user
    @auth.login_required
    @marshal_with(user_fields)
    def delete(self, id):
        user=session.query(UserModel).filter(UserModel.id == id).first()
        if user is None:
            abort(404, status="fail", message="No such user")
        elif (user.user != request.authorization.username):
            abort(403, status="fail", message="Only current logged user can be deleted")
        else:
            # Abort if any operation exist to deleted user
            operation = session.query(OperationModel).filter(OperationModel.user_id == user.id).first()
            if operation is not None:
                abort(424, status="fail", message="Cannot be deleted, has related records in operations")
            else:
                curr_sess=db.session.object_session(user)
                curr_sess.delete(user)
                curr_sess.commit()
                return user, 204

#  View uploaded and generated resources
class UploadResource(Resource):
    @auth.login_required
    def get(self, filename):
        
        if not os.path.exists(os.path.join(BASEDIR, UPLOAD_FOLDER, filename)):
            abort(404, status="fail", message="No such file")

        file_link=os.path.join(APP_URL, UPLOAD_FOLDER, filename)
        user=session.query(UserModel).filter(UserModel.user == request.authorization.username).first()
        operation=session.query(OperationModel).filter(or_(OperationModel.generated_file == file_link, OperationModel.original_file == file_link, OperationModel.keyword == file_link)).first()

        # Check if the file belong to current user
        if operation is None or operation.user_id != user.id:
            abort(403, status="fail", message="Current user is not owner of that file")
        
        return send_from_directory(os.path.join(BASEDIR, UPLOAD_FOLDER),filename)

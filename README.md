# Usage


### Authentication method

Basic Authentication with `user` and `password`

## User

### Create user
First needed to create user with 

`POST /user`

Query Parameters
* user - Desired of username
* password - Desired password

This user and password will be used on *every query* except this one in order to authenticate access rights


### Get current user parameters
The current user parameters can be queried with 

`GET /user`

Query Parameters
* None


### Delete selected user 
Also possible to delete user if you are authenticated to do that

`DELETE /user/<int: id>`

Query Parameters
* None

Keep in mind that if you will delete user all related operations data including files also will be deleted



## Operations


### Create operation
In order to replace special keywords with their tradmarked replacement you need to create operation with

`POST /operations`

Query Parameters
* file - Document file
* keyword - Keyword file

### Return all operation
The current user parameters can be queried with 

`GET /operations`

Query Parameters
* None

### Return selected operation
To return selected operations parameters 

`GET /operations/<int: id>`

Query Parameters
* None

### Delete selected operation
To delete selected operation

`GET /operations/<int: id>`


## Uploaded files

### get content uploaded file
In order to read file

`GET /uploads/<string: filename>`



## Installation

### 1. Prerequisites
```
    python 3
    virtualenv
    pip
    git
```
### 2. Clone from github
```
git clone 
```

### 3. Create virtualenv
```
python3 -m venv venv
```

### 4. Activation and setting of virtual environment 
```
source .env
```

### 5. Install requirements of application
```
pip install -r requirements.txt
```

### 6. Create database and tabless inside
```
python3 manage.py create_folder
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```
### 7. Run application
```
python run.py
```

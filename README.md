# Getting started

## Usage

### Authentication


### User

Get curren user

`GET /user`


Query Parameters
* None


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
pyton3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```
### 7. Run application
```
python run.py
```

### ps:  _Application will run on port 5000 by default_


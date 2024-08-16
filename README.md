
# Run application without docker
INFO: All related to Python will be setup IN and FROM the backend/ directory!

## Step 1 → Open your project root directory and set up your Python via PyEnv:
```
pyenv install 3.11.0
```
## Step 2 → Create our virtual environment:
```
pyenv virtualenv 3.11.0 YOUR_VENV_NAME
```
## Step 3 → Set the newly created virtual environment as your main Python interpreter in the root directory:

```
 pyenv local YOUR_VENV_NAME
```
## Step 4 →  Install the initial project requirements with pip3:
```
pip3 install -r requirements.txt
```
## Step 5 →  INIT ENV VARIABLES:
 setup env by creating ".env" file
 given example in ".env.example"

## Step 6 →  Run Application :
```
  uvicorn src.main:backend_app --reload 
```

<br>

# Database migration

## Step1 → initialize alembic migrations
```
 alembic init
```
## Step 2 → Create the initialization of your database migration:
```
alembic revision --autogenerate -m "YOUR NOTES ABOUT THE DATABASE MIGRATION HERE"
```
## Step 3 → Push the registered database objects to your database:
```
alembic upgrade head
```
<br>

# Run with Docker 

```
  docker compose up -d
```
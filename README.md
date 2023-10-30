# promos-api
Python API 

# Run the app in Docker
`docker build -t promos-api .`

`docker run --network host -p 5000:5000 -v $(pwd):/app -e FLASK_APP=main.py promos-api`

## Creating the .env file:
```
DB_USERNAME=""
DB_PASSWORD=""
DB_HOST=""
DB_NAME=""
JWT_SECRET_KEY=""
```

## Running the venv:
`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

## Running the migrations:
`alembic upgrade head`

## If you need to create a migration:
`alembic revision --autogenerate -m "Migration name"`

## If you need to revert a migration:
`alembic downgrade base`
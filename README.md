## CircleCI:
[![CircleCI](https://circleci.com/gh/mohamedtosman/pizza-shop.svg?style=shield)](https://circleci.com/gh/mohamedtosman/pizza-shop)

## Project

A pizza shop API that supports two roles:

`READONLY` which are unauthenticated users that are able to only view and list pizza flavors and orders.

`ADMIN`  which are authenticated users that are able to create/update/delete pizza flavors and orders on top of also viewing and listing them.

## Technologies

  - Django
  - Docker Compose
  - Docker
  - Python3
  - PostgreSQL
  - Swagger
  - Pylint
  - CircleCI

## Instructions

Make sure that docker-compose and docker are installed on your system. Clone the repository and then change directory to the cloned repository.

Execute the API using docker-compose

```
docker-compose up api
```

Create a superuser which will be used for the ADMIN role

```
docker-compose exec api python manage.py createsuperuser
```

Execute the database migrations and load initial pizza flavors into the database

```
docker-compose exec api python manage.py migrate
docker-compose exec api python manage.py loaddata pizzas.json
```

You can now reach the application at

```
http://localhost:8000/api/
```

To use the application using `READONLY` role, no further action is needed, but you will be
able to reach GET endpoints.

To use the application using `ADMIN` role, please login with superuser credentials created above by clicking on
`Login` on the top right hand corner of the application. Now you will be able to reach
all endpoints.

## Tests

Execute the tests using docker-compose

```
docker-compose up test
```

The tests are integrated into CircleCI, so they are executed automatically whenever a new commit is pushed.

## API Documentation

Swagger was used to document all endpoints. You can access it at

```
http://localhost:8000/docs/
```

All `GET` endpoints will be initially displayed unless user is authenticated/logged in first on the application.

## API Examples for Creating & Updating Endpoints

### Create Order

- `POST /orders/`

```
{
  "customer": {
    "name": "John Doe",
    "address": "123 Address",
    "phone": "123-456-789"
  },
  "pizzas": [{
    "id": "6cf64e9a-9871-412a-ab4d-173a92af270f",
    "details": [{
      "size": "Small",
      "count": 3
    }, {
      "size": "Medium",
      "count": 2
    }]
  }]
}
```

### Update Order

- `PUT /orders/<order_id>/`

```
{
  "customer": {
    "name": "John Doe",
    "address": "123 Address",
    "phone": "123-456-789"
  },
  "pizzas": [{
    "id": "6cf64e9a-9871-412a-ab4d-173a92af270f",
    "details": [{
      "size": "Small",
      "count": 3
    }, {
      "size": "Large",
      "count": 2
    }]
  }]
}
```

### Update Status

- `PUT /orders/<order_id>/status/`

```
{
    "status": "Delivered"
}
```

### Get Filtered Orders

- `GET /orders/<order_id>/status/?status=<status>&customer=<customer>`

## Linters & Formatters

PyLint-django plugin was used to lint the application and further analyze code for proper code formatting and structure.
PyLint is integrated into CircleCI to automatically run whenever a new commit is pushed.
However, if you wish to run locally, please execute:

```
pylint --load-plugins pylint_django api --rcfile=.pylintrc
```

## Continuous Integration (CI)

CircleCI was integrated on my github account to run the tests and linter whenever a new commit is pushed.
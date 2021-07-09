# TkRecipes API

## About

Tk Recipes is a CRUD API with Django and DRF that allows you to create, read, update and delete recipes and add/delete ingredients to it.

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/ivankzl/tk-recipes-backend.git
$ cd tk-recipes-backend
```

Then you can run the docker image:


```sh
$ docker-compose up
```

Once your docker image is up and running, you can test the API by using Postman, CURL or your favourite tool, sending your requests to the root URL `http://127.0.0.1:8000/`. The available endpoints you can hit are the following:

- List all the recipes
    - **GET** /api/recipe/recipes/
- Filter recipes by name (case insensitive)
    - **GET** /api/recipe/recipes/?name=`<query>`/
- Get a particular recipe by key
    - **GET** /api/recipe/recipes/`<pk>`/
- Create a new recipe
    - **POST** /api/recipe/recipes/
- Full-edit a recipe
    - **PATCH** /api/recipe/recipes/`<pk>`/
- Partially edit a recipe
    - **PUT** /api/recipe/recipes/`<pk>`/ 
- Delete a recipe
    - **DELETE** /api/recipe/recipes/`<pk>`/

### Example: Create a new Recipe

POST /api/recipe/recipes/

Request body:

    {
        'name': 'Gnocchi',
        'description': 'A detailed description of a yummy recipe!',
        'ingredients': [
            {'name': 'Potatoes'},
            {'name': 'Flour'},
            {'name': 'Nutmeg'}
        ]
    }


## Tests

To run the tests you can execute:
```sh
docker-compose run --rm app sh -c "python manage.py test"
```
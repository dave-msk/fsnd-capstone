# Casting Agency API - Udacity Full-Stack Developer Nanodegree

This repository contains the capstone project of [Udacity Full-Stack Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044) program.

The project is structured as follows:

```
├── README.md
├── requirements.txt
├── app
│   ├── app.py
│   ├── manage.py
│   ├── core/
│   └── migrations/
└── postman/
```

The `app` directory contains the application, while the `postman` directory contains Postman collections for RBAC tests.

## How to run

### Install Dependencies

This project is built upon Python **3.7**. Dependencies can be installed by running:


```bash
$ pip install -r requirements.txt
```

### Setup Database

Set the PostgreSQL database URL to the environment variable `DATABASE_URI`, and run the following from `<project_root>/app`:

```bash
$ python manage.py db upgrade
```

### Start API Server

Run the following command from `<project_root>/app` to start the local server for development:

```bash
$ python app.py
```

The server will listen on port 8080, which is used by the Postman test cases.

## Tests

### Unit Tests

The unit tests are named as `<module>_test.py`. To run all the unit tests, execute the following from `<project_root>/app`:

```bash
$ python -m unittest discover -p "*_test.py"
```

### RBAC Tests

The RBAC tests require a JWT token from Auth0. Three testing account has been created and included in their respective Postman collection. Run the Postman collections, located in [`postman/`](./postman), to perform the RBAC tests on the local development server.


## Roles

There are three roles in total - `casting-agency/casting-assistant`, `casting-agency/casting-director`, `casting-agency/executive-producer`.

The `casting-agency/casting-assistant` role is granted permissions for read-only actions that do not affect state, such as viewing actors and movies.

The `casting-agency/casting-director` is granted all permissions of `casting-agency/casting-assistant`, plus permissions for adding, deleting and modifying actors, and modifying (but not adding or deleting) movies.

The `casting-agency/executive-producer` role is granted all permissions of `casting-agency/casting-director`, plus adding & deleting movies.

The table of permissions granted to each role is given by:

| Roles | Permissions |
|:-:|:-:|
| `casting-agency/casting-assistant` | `get:actors`<br>`get:movies` |
| `casting-agency/casting-director`  | `get:actors` <br> `get:movies` <br> `post:actors` <br> `patch:actors` <br> `patch:movies` <br> `delete:actors` |
| `casting-agency/executive-producer`  | `get:actors` <br> `get:movies` <br> `post:actors` <br> `post:movies` <br> `patch:actors` <br> `patch:movies` <br> `delete:actors` <br> `delete:movies` |

## API Endpoints

This section contains details of each API endpoint.

### Errors

- `400`: If any of the required JSON input items is missing, or it contains items with values of invalid type.
- `401`: Unauthorized access.
- `404`: If the specified resource (involving URL parameters) does not exist.
- `422`: If the JSON input contains items with unprocessable values.
- `500`: Unexpected server errors.

The errors above have the following return body:

```json
{
  "success": false,
  "error": <error_code>,
  "message": "Error message"
}
```

### GET `/actors`
- Description: Retrieve all actors
- Permission: `get:actors`

- Returns:

  ```json
  {
    "success": true,
    "actors": [
      {"id": 1,
        "name": "Actor Name",
        "age": 30,
        "gender": "F",
        "movies": [
          {"id": 1, "title": "Movie Title"},
          ...
        ]
      }
    ]
  }
  ```

### GET `/movies`
- Description: Retrieve all movies
- Permission: `get:movies`

- Returns:

  ```json
  {
    "success": true,
    "movies": [
      {
        "id": 1,
        "title": "Movie Title",
        "release_date": "1970-01-01",
        "actors": [
          {"id": 1, "name": "Actor name"},
          ...
        ]
      }
    ]
  }
  ```

### POST `/actors`
- Description: Create a new actor
- Permission: `post:actors`
- Inputs:

  ```json
  {
    "name": "Actor Name",  // required, string
    "age": 18,             // required, integer
    "gender": "M",         // required, "M" or "F"
    "movies": [3, 7]       // optional, [integers], movie IDs
  }
  ```

- Returns:
  ```json
  {
    "success": true,
    "actor": {
      "id": 2,  // dynamically assigned
      "name": "Actor Name",
      "age": 18,
      "gender": "M",
      "movies": [
        {"id": 3, "title": "Movie 3"},
        {"id": 7, "title": "Movie 7"}
      ]
    }
  }
  ```

### POST `/movies`
- Description: Create a new movie
- Permission: `post:movies`
- Inputs:

  ```json
  {
    "title": "Movie Title",        // required, string
    "release_date": "1970-01-01",  // required, string, "YYYY-MM-DD"
    "actors": [2, 4]               // optional, [integers], actor IDs
  }

- Returns:

  ```json
  {
    "success": true,
    "movie": {
      "id": 9,  // dynamically assigned
      "title": "Movie Title",
      "release_date": "1970-01-01",
      "actors": [
        {"id": 2, "name": "Actor 2"},
        {"id": 4, "name": "Actor 4"}
      ]
    }
  }
  ```

### PATCH `/actors/{actor_id}`:
- Description: Update an existing actor
- Permission: `patch:actors`
- Inputs:

  ```json
  {
    "name": "New Name",  // optional, string
    "age": 19,           // optional, integer
    "gender": "F",       // optional, "M" or "F"
    "movies": [3, 7, 8]  // optional, [integers], movie IDs
  }
  ```

- Returns:
  
  ```json
  {
    "success": true,
    "actor": {
      "id": <actor_id>,
      "name": "New Name",
      "age": 19,
      "gender": "F",
      "movies": [
        {"id": 3, "title": "Movie 3"},
        {"id": 7, "title": "Movie 7"},
        {"id": 9, "title": "Movie 9"}
      ]
    }
  }
  ```

### PATCH `/movies/{movie_id}`:
- Description: Update an existing movie
- Permission: `patch:movies`
- Inputs:

  ```json
  {
    "title": "New Title",          // optional, string
    "release_date": "1970-06-30",  // optional, string, "YYYY-MM-DD"
    "actors": [2, 4, 8]            // optional, [integers], actor IDs
  }

- Returns:

  ```json
  {
    "success": true,
    "movie": {
      "title": "New Title",
      "release_date": "1970-06-30",
      "actors": [
        {"id": 2, "name": "Actor 2"},
        {"id": 4, "name": "Actor 4"},
        {"id": 8, "name": "Actor 8"}
      ]
    }
  }

### DELETE `/actors/{actor_id}`:
- Description: Delete an existing actor
- Permission: `delete:actors`
- Returns:

  ```json
  {
    "success": true,
    "actor_id": <actor_id>
  }
  ```

### DELETE `/movies/{movie_id}`:
- Description: Delete an existing actor
- Permission: `delete:movies`
- Returns:

  ```json
  {
    "success": true,
    "movie_id": <movie_id>
  }
  ```

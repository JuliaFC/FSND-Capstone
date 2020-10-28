# Welcome to the Starkiller Base Backend

This app works as a tool for the members of the First Order to access info on their crew and the available bases for their operation.

## PIP Dependencies

Install dependencies by naviging to the project root directory and running:

```bash
$ pip install -r requirements.txt
```

This will install all of the required packages which are selected within the `requirements.txt` file.

## Key Dependencies

- [Flask](http://flask.pocoo.org/)  

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) 

- [jose](https://python-jose.readthedocs.io/en/latest/)

- [PostgresSQL](https://www.postgresql.org/download/)

## Working Directory
Go to the directory where you check out the [repository](https://github.com/JuliaFC/FSND-Capstone) which includes First Order backend code.

## Running the server

### Running the server from localhost
Make sure you are have installed the dependencies and **PostgreSQL** is running on port 5432 before you start running the server. Go to the root directory, then run the following commands:

```bash
$ chmod +x setup.sh
$ ./setup.sh
```

### Deployment on Heroku
The app's backend server is deployed on Heroku. You can visit and interact with the app's backend server via: 

https://capstone-fsnd-jf.herokuapp.com/. 

In order to test the APIs,  use Postman with proper authentication information. For Postman, the authentication tokens have been included in [Capstone_Collection.json](https://github.com/JuliaFC/FSND-Capstone/blob/master/Capstone_Collection.json).

The default host is set to https://capstone-fsnd-jf.herokuapp.com/ in the collection variables. If you want to test APIs with Heroku deployment, you can update the collection variable `server_url` to http://127.0.0.1:5000 in Postman.

## Data modeling
**model.py** includes database schema and helper functions such as insert, update, delete and format functions. There are two tables created in the database: **Base** and **Crew**. Only the Supreme Leader can can create, update and delete entries from all tables. Crew users can only view the entries in the two tables. 

#### Base

A Base object describes a `base` with attributes as `name`, `planet` and `crew`, which act as a location where the First Order is settled.

#### Crew

A Crew object describes a member with attributes as `name`, `rank`, `date_of_birth`, `bio` and `base_id` of the First Order.

## API use cases

### Supreme Leader
* Only users with the **Supreme Leader token** have all the admin permissions. Refer to **Retrieve tokens via Auth0** section below which mentions how to retrieve that token. 

* Supreme Leader users can perform all CRUD operations on Base and Crew via [POST, GET, PATCH, DELETE] `/base/ and `/crew`. 

Please note that because of the relationship, a Base needs to be created first if you wish to add a Crew member to it, via the attribute `base_id`.


### Crew
* Crew members can only perform get operations via `GET /crew` and `GET /base`.

## API endpoints

### Crew
The following API allows you to get, post, delete and update Crew data. 

#### GET '/crew'
- Fetches a list of  members from the existing crew collection.
- No request arguments are required.
- Returns a list of id and crew pairs.

##### Exmaple request:
`GET /crew`

##### Exmaple response:

```javascript
{
    "crew": [
        {
            "base_id": 1,
            "bio": "Supreme Leader of the First Order",
            "date_of_birth": "Sat, 17 Dec 5 00:00:00 GMT",
            "id": 1,
            "name": "Kylo Ren",
            "rank": "Commander"
        }
    ],
    "success": true
}
```

#### POST '/crew'
- Requires **Supreme Leader** authentication.
- Creates a new crew in the existing crew collection.
- No request arguments are required.
- Data in the body is required.
- Returns a newly added crew and success status.

##### Exmaple request with data in the body:
`POST /crew`

```javascript
{
    "name": "Kylo Ren",
    "rank": "Commander",
    "date_of_birth": "0005-12-17",
    "bio": "Supreme Leader of the First Order",
    "base_id": "1"
}

```

##### Exmaple response:
```javascript
{
    "crew": {
        "base_id": 1,
        "bio": "Supreme Leader of the First Order",
        "date_of_birth": "Sat, 17 Dec 5 00:00:00 GMT",
        "id": 1,
        "name": "Kylo Ren",
        "rank": "Commander"
    },
    "success": true
}
```

#### DELETE '/crew/{crew_id}'
- Requires **Supreme Leader** authentication.
- Deletes a specified crew based on the `crew_id`.
- Request arguments: `crew_id`
- Returns the deleted `crew` and success status.

##### Exmaple request:
`DELETE /crew/1`

##### Exmaple response:

```javascript
{
    "delete": 1,
    "success": true
}
```

#### PATCH '/crew/{crew_id}'
- Requires **Supreme Leader** authentication.
- Updates a specified question based on the `crew_id`
- Request arguments: `crew_id`
- Data in the body is required.
- Returns an updated crew information and success status.

##### Exmaple request with data in the body:
`PATCH /crew/1`

```javascript
{
    "name": "Kylo Ren",
    "rank": "Supreme Leader",
    "date_of_birth": "0005-12-17",
    "bio": "Supreme Leader of the First Order",
    "base_id": "1"
}

```

##### Exmaple response:
```javascript
{
    "crew": {
        "base_id": 1,
        "bio": "Supreme Leader of the First Order",
        "date_of_birth": "Sat, 17 Dec 5 00:00:00 GMT",
        "id": 2,
        "name": "Kylo Ren",
        "rank": "Supreme Leader"
    },
    "success": true
}
```

### Base
The following API allows you to get, post, delete and update Base data. 


#### GET '/base'
- Fetches a list of base from the existing base collection.
- No request arguments are required.
- Returns a list of base including `id`, `name`, `planet` and `crew` key:value pairs and success status.

##### Exmaple request:
`GET /base`

##### Exmaple response:

```javascript
{
    "base": [
        {
            "crew": [
                {
                    "base_id": 1,
                    "bio": "Supreme Leader of the First Order",
                    "date_of_birth": "Sat, 17 Dec 5 00:00:00 GMT",
                    "id": 2,
                    "name": "Kylo Ren",
                    "rank": "Supreme Leader"
                }
            ],
            "id": 1,
            "name": "Death Star",
            "planet": "Endor"
        }
    ],
    "success": true
}
```

#### POST '/base'
- Requires **Supreme Leader** authentication.
- Creates a new base in the existing base collection.
- No request arguments are required.
- Data in the body is required.
- Returns a newly added base and success status.

##### Exmaple request with data in the body:
`POST /base`

```javascript
{
    "name": "Death Star",
    "planet": "Endor"
}
```

##### Exmaple response:
```javascript
{
    "base": {
        "crew": [],
        "id": 1,
        "name": "Death Star",
        "planet": "Endor"
    },
    "success": true
}
```

#### DELETE '/base/{base_id}'
- Requires **Supreme Leader** authentication.
- Deletes a specified base based on the `base_id`.
- Request arguments: `base_id`
- Returns the deleted `base` and success status.

##### Exmaple request:
`DELETE /base/2`

##### Exmaple response:

```javascript
{
    "delete": 1,
    "success": true
}
```

#### PATCH '/base/{base_id}'
- Requires **Supreme Leader** authentication.
- Updates a specified base based on the `base_id`
- Request arguments: `base_id`
- Data in the body is required and includes the base's attributes to update.
- Returns a base with the updated attributes and success status.

##### Exmaple request with data in the body:
`PATCH /base/1`

```javascript
{
    "name": "Death Star II",
    "planet": "Endor"
}
```

##### Exmaple response:
```javascript
{
    "base": {
        "crew": [],
        "id": 2,
        "name": "Death Star II",
        "planet": "Endor"
    },
    "success": true
}
```


## Testing

### Test.py
In order to test the backend server, go to the working directory and run the following command.

```bash
$ chmod +x test_setup.sh
$ ./test_setup.sh
```

### Retrieve tokens via Auth0
Authentication tokens included in **test_setup.sh** and [Capstone_Collection.json](https://github.com/JuliaFC/FSND-Capstone/blob/master/Capstone_Collection.json) will expire in **24** hours. Once the tokens expire, please use the following Auth0 link to retrieve the updated tokens accordingly. 

**Auth0 link**:
https://cowffeeshop.us.auth0.com/authorize?audience=capstone-api&response_type=token&client_id=9thObDYilxkxjY8cWvynTiF4hjH5vyxD&redirect_uri=https://127.0.0.1:5000

**Supreme Leader login**: supremeleader@firstorder.com / password: *Capstone123

**Crew login**: crew@firstorder.com / password: *Capstone123

Make sure you clear the browser cache before you login with link above. After you login, you will see the following link as the browser address. The token is the value of "access_token". So copy the value between "access_token=" and "&expires_in=86400&token_type=Bearer". That's the token we use in Postman and test_setup.sh.

Valid tokens are required before using the app. Open Postman -> What_to_eat_heroku_deployment -> Supreme Leader -> Edit -> Authorization tab, update the old token with the new token in the Token section. Under User folder in Postman, follow the same steps to update User's token in Postman. Then you should be able test the app in different roles.
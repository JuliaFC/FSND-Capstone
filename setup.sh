#!/bin/sh -x

DATABASE_NAME='capstone_fsnd'
if ! psql -lqt | cut -d \| -f 1 | grep -qw $DATABASE_NAME; then
    echo "A database with the name $DBNAME does not exist."
    createdb $DATABASE_NAME
fi

# Export the environment variables and set up for the server
export AUTH0_DOMAIN='cowffeeshop.us.auth0.com'
export API_AUDIENCE='capstone-api'
export ALGORITHMS=['RS256']
export DATABASE_URL='postgresql://localhost:5432/capstone_fsnd' 
export PGGSSENCMODE=disable 
export FLASK_APP=app.py 
export FLASK_ENV=development 
flask run
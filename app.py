import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import db_drop_and_create_all, DATABASE_PATH, Crew, Base
from auth import AuthError, requires_auth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_PATH

db = SQLAlchemy(app)
CORS(app, resources={r"/app/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Origin',
        'http://127.0.0.1:8100')
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PUT,POST,PATCH,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

def change(new, current):
    if new is None or not new:
        return current
    if current != new and new:
        return new
    return current

# ROUTES

# @app.route('/')
# def hello_app():
#     return jsonify({
#         "success": True,
#         "message": "Hello, to proceed check the documentation!"
#     })

@app.route('/crew', methods=['GET'])
@requires_auth('get:crew')
def get_crew(token):
    crew = Crew.query.all()
    if crew is None:
        abort(404)
    else:
        crew = [c.format() for c in crew]
    return jsonify({
        "success": True,
        "crew": crew
    })

@app.route('/crew/<int:crew_id>', methods=['GET'])
@requires_auth('get:crew')
def get_crew_by_id(token, crew_id):
    try:
        crew = Crew.query.get(crew_id)
        if crew is None:
            return json.dumps({
                "success":
                False,
                "error":
                'Crew #' + str(crew_id) + ' not found'
            }), 404

        return jsonify({
            "success": True,
            "crew": crew
        })
    except BaseException:
        abort(500)

@app.route('/crew', methods=['POST'])
@requires_auth('post:crew')
def add_crew_member(token):

    body = request.get_json()
    name = body.get('name')
    rank = body.get('rank')
    date_of_birth = body.get('date_of_birth')
    bio = body.get('bio')
    base_id = body.get('base_id')

    if (name is None) or (rank is None):
        abort(422)

    try:
        new_crew_member = Crew(
            name=name,
            rank=rank,
            date_of_birth=date_of_birth,
            bio=bio,
            base_id=base_id)
        new_crew_member.insert()
        new_crew_member = new_crew_member.format()
        return jsonify({
            "success": True,
            "crew": new_crew_member
        })
    except IndexError:
        abort(500)

@app.route('/crew/<int:crew_id>', methods=['PATCH'])
@requires_auth('patch:crew')
def edit_crew_member(token, crew_id):
    try:
        crew = Crew.query.get(crew_id)
        if crew is None:
            return json.dumps({
                "success":
                False,
                "error":
                'Crew #' + str(crew_id) + ' not found to be edited'
            }), 404

        body = request.get_json()
        name = body.get('name')
        rank = body.get('rank')
        date_of_birth = body.get('date_of_birth')
        bio = body.get('bio')
        base_id = body.get('base_id')

        crew.name = change(name, crew.name)
        crew.rank = change(rank, crew.rank)
        crew.date_of_birth = change(date_of_birth, crew.date_of_birth)
        crew.bio = change(bio, crew.bio)
        crew.base_id = change(base_id, crew.base_id)
        crew.update()
        crew = crew.format()

        return jsonify({
            "success": True,
            "crew": crew
        })

    except IndexError:
        abort(422)

@app.route('/crew/<int:crew_id>', methods=['DELETE'])
@requires_auth('delete:crew')
def delete_crew_member(token, crew_id):
    crew = Crew.query.get(crew_id)
    if not crew or crew is None:
        return json.dumps({
            "success":
            False,
            "error":
            'Crew #' + str(crew_id) + ' not found to be deleted'
        }), 404
    else:
        crew.delete()

    return jsonify({
        "success": True,
        "delete": crew_id
    })

@app.route('/base', methods=['GET'])
@requires_auth('get:base')
def get_base(token):
    base = Base.query.all()
    if base is None:
        abort(404)
    else:
        base = [b.format() for b in base]
    return jsonify({
        "success": True,
        "base": base
    })

@app.route('/base/<int:base_id>', methods=['GET'])
@requires_auth('get:base')
def get_base_by_id(token, base_id):
    try:
        base = Base.query.get(base_id)
        if base is None:
            return json.dumps({
                "success":
                False,
                "error":
                'Base #' + str(base_id) + ' not found'
            }), 404

        return jsonify({
            "success": True,
            "base": base
        })
    except BaseException:
        abort(500)

@app.route('/base', methods=['POST'])
@requires_auth('post:base')
def add_base(token):

    body = request.get_json()
    name = body.get('name')
    planet = body.get('planet')

    if name is None or planet is None:
        abort(422)

    try:
        new_base = Base(name=name, planet=planet)
        new_base.insert()
        new_base = new_base.format()
        return jsonify({
            "success": True,
            "base": new_base
        })
    except BaseException:
        abort(500)

@app.route('/base/<int:base_id>', methods=['PATCH'])
@requires_auth('patch:base')
def edit_base(token, base_id):
    try:
        base = Base.query.get(base_id)
        if base is None:
            return json.dumps({
                "success":
                False,
                "error":
                'Base #' + str(base_id) + ' not found to be edited'
            }), 404

        body = request.get_json()
        name = body.get('name')
        planet = body.get('planet')

        base.name = change(name, base.name)
        base.planet = change(planet, base.planet)

        base.update()
        base = base.format()

        return jsonify({
            "success": True,
            "base": base
        })

    except IndexError:
        abort(422)

@app.route('/base/<int:base_id>', methods=['DELETE'])
@requires_auth('delete:base')
def delete_base(token, base_id):
    base = Base.query.get(base_id)
    if not base or base is None:
        return json.dumps({
            "success":
            False,
            "error":
            'Base #' + str(base_id) + ' not found to be deleted'
        }), 404
    else:
        base.delete()

    return jsonify({
        "success": True,
        "delete": base_id
    })

# Error Handling

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable entity"
    }), 422

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }), 500

@app.errorhandler(AuthError)
def auth_error(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.run()
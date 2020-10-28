import os
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

import json

DATABASE_NAME = "capstone_fsnd"
DATABASE_PATH = "postgres://jdvxulnfaygqjx:d870caa344200225a06901b7d3a88dd739924f43327e00bea57fa225795896b4@ec2-54-158-222-248.compute-1.amazonaws.com:5432/d6tehd0ugf08lv"
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=DATABASE_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CORS_SUPPORTS_CREDENTIALS"] = True
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple versions of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Crew
a persistent crew entity, extends the base SQLAlchemy Model
'''


class Crew(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rank = Column(String, nullable=False)
    date_of_birth = Column(Date)
    bio = Column(String)
    base_id = Column(Integer, ForeignKey('base.id'))

    '''
    insert()
        inserts a new model into a database
        EXAMPLE
            crew = Crew(name=req_name, rank=req_rank)
            crew.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            crew = Crew(name=req_name, rank=req_rank)
            crew.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            crew = Crew.query.filter(Crew.id == id).one_or_none()
            crew.rank = 'General'
            crew.update()
    '''

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'rank': self.rank,
            'date_of_birth': self.date_of_birth,
            'bio': self.bio,
            'base_id': self.base_id
        }

    def __repr__(self):
        return json.dumps(self.format())


class Base(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    planet = Column(String, nullable=False)
    crew = relationship("Crew")

    '''
    insert()
        inserts a new model into a database
        EXAMPLE
            base = Base(name=req_name, planet=req_planet)
            base.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            base = Base(name=req_name, planet=req_planet)
            base.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            base = Base.query.filter(Base.id == id).one_or_none()
            base.planet = 'Ilum'
            base.update()
    '''

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'planet': self.planet,
            'crew': [c.format() for c in self.crew],
        }

    def __repr__(self):
        return json.dumps(self.format())

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os

import flask_sqlalchemy as fsk_db


def setup_db(app, database_path=None):
  if database_path is None: database_path = os.environ["DATABASE_URL"]
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  
  db = fsk_db.SQLAlchemy()
  db.app = app
  db.init_app(app)
  models = create_models(db)
  db.create_all()

  return db, models


def create_models(db):
  gender_t = db.Enum("M", "F", name="gender_t")

  movie_actor_asso = db.Table(
      "movie_actor_association",
      db.Column("movie_id", db.Integer, db.ForeignKey("movie.id")),
      db.Column("actor_id", db.Integer, db.ForeignKey("actor.id")))

  # Movies
  class Movie(db.Model):
    __tablename__ = "movie"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date(), nullable=False)

    actors = db.relationship("Actor",
                             secondary=movie_actor_asso,
                             back_populates="movies")

  # Actors
  class Actor(db.Model):
    __tablename__ = "actor"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(gender_t, nullable=False)

    movies = db.relationship("Movie",
                             secondary=movie_actor_asso,
                             back_populates="actors")

  Models = collections.namedtuple("Models", ["Movie", "Actor"])
  return Models(Movie, Actor)

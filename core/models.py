from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask_sqlalchemy as fsk_db


db = fsk_db.SQLAlchemy()
_movie_actor = db.Table(
    "movie_actor_association",
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id")),
    db.Column("actor_id", db.Integer, db.ForeignKey("actor.id")))


class Movie(db.Model):
  __tablename__ = "movie"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=False)
  release_date = db.Column(db.Date(), nullable=False)

  actors = db.relationship("Actor",
                           secondary=_movie_actor,
                           back_populates="movies")

  def format(self):
    return {"id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "actors": self.actors}


class Actor(db.Model):
  __tablename__ = "actor"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  age = db.Column(db.Integer, nullable=False)
  gender = db.Column(db.Enum("M", "F", name="gender_t"), nullable=False)

  movies = db.relationship("Movie",
                           secondary=_movie_actor,
                           back_populates="actors")

  def format(self):
    return {"id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "movies": self.movies}

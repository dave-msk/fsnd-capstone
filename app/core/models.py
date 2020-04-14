# Copyright 2020 Siu-Kei Muk (David). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

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
  title = db.Column(db.String(64), nullable=False)
  release_date = db.Column(db.Date(), nullable=False)

  actors = db.relationship("Actor",
                           secondary=_movie_actor,
                           back_populates="movies")

  def format(self):
    return {"id": self.id,
            "title": self.title,
            "release_date": self.release_date.isoformat(),
            "actors": [{"id": a.id, "name": a.name} for a in self.actors]}


class Actor(db.Model):
  __tablename__ = "actor"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
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
            "movies": [{"id": m.id, "title": m.title} for m in self.movies]}


def is_gender(gender):
  return gender in {"F", "M"}

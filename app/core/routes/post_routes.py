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

import datetime

import flask

from core import models
from core import utils
from core.routes import routebase


def gather_post_route_details():
  desc = {
      "short": "Factory of POST-routes for Casting Agency API",
      "long":
          """Creates a POST-route for Casting Agency API.
          
          Available routes:
          
            - actor: POST /actors
            - movie: POST /movies
          """,
  }

  sig = {
      "key": {
          "type": str,
          "description": "Route key, one of [\"actor\", \"movie\"].",
      },
  }
  sig.update(routebase.Route._SIG)  # pylint: disable=protected-access

  return {"factory": PostRoute, "sig": sig, "descriptions": desc}


class PostRoute(routebase.Route):
  def __init__(self, key, permission=None):
    route, fn = globals()["make_post_%s" % key]()
    super(PostRoute, self).__init__(route, fn, "POST", permission=permission)


def make_post_actor():
  def post_actor():
    data = utils.get_json()

    # Validate input keys
    if (any(k not in data for k in {"name", "age", "gender"}) or
        any(k not in {"name", "age", "gender", "movies"} for k in data)):
      flask.abort(400)

    # Validate input values and construct actor
    args = {
        "name": utils.validate_and_convert(data["name"], str),
        "age": utils.validate_and_convert(data["age"], int),
        "gender": utils.validate_and_convert(data["gender"], str,
                                             convert_fn=lambda g: g.upper(),
                                             test_fn=models.is_gender,
                                             cast=True),
    }

    # Convert movie IDs to Movie objects
    if "movies" in data:
      args["movies"] = utils.validate_and_convert(
          data["movies"], [int],
          convert_fn=lambda ids: [models.Movie.query.get(mid) for mid in ids],
          test_fn=lambda ms: all(m is not None for m in ms),
          cast=True)

    actor = models.Actor(**args)

    try:
      models.db.session.add(actor)
      models.db.session.commit()
    except:
      models.db.rollback()
      raise

    return flask.jsonify({
        "success": True,
        "actor": actor.format(),
    })

  return "/actors", post_actor


def make_post_movie():
  def post_movie():
    data = utils.get_json()

    # Validate input keys
    if (any(k not in data for k in {"title", "release_date"}) or
        any(k not in {"title", "release_date", "actors"} for k in data)):
      flask.abort(400)

    # Validate input values and construct actor
    args = {
        "title": utils.validate_and_convert(data["title"], str),
        "release_date": utils.validate_and_convert(
            data["release_date"], str,
            convert_fn=lambda s: datetime.datetime.fromisoformat(s)),
    }

    # Convert actor IDs to Actor objects
    if "actors" in data:
      args["actors"] = utils.validate_and_convert(
          data["actors"], [int],
          convert_fn=lambda ids: [models.Actor.query.get(aid) for aid in ids],
          test_fn=lambda a_lst: all(a is not None for a in a_lst))

    movie = models.Movie(**args)

    try:
      models.db.session.add(movie)
      models.db.session.commit()
    except:
      models.db.rollback()
      raise

    return flask.jsonify({
        "success": True,
        "movie": movie.format(),
    })

  return "/movies", post_movie

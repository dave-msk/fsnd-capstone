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
      "short": "",
      "long":
          """
          """,
  }

  sig = {
      "key": {
          "type": str,
          "description": "",
      },
  }
  sig.update(routebase.Route._SIG)  # pylint: disable=protected-access

  return {"factory": PostRoute, "sig": sig, "descriptions": desc}


class PostRoute(routebase.Route):
  def __init__(self, key, permission=None):
    super(PostRoute, self).__init__(permission=permission)
    self._method = "POST"
    self._route, self._fn = globals()["make_post_%s" % key]()


def make_post_actor():
  def post_actor():
    data = utils.get_json()
    spec = {"name": str, "age": int, "gender": str}
    base = utils.validate_data(data, spec, cast=True)
    actor = models.Actor(**base)
    if "movies" in data:
      if len(data) > 4: flask.abort(400)
      movies = utils.validate_data(data["movies"], [int], cast=True)
      actor.movies = movies
    else:
      if len(data) != 3: flask.abort(400)

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
    spec = {"title": str, "release_date": str}
    base = utils.validate_data(data, spec, cast=True)
    base["release_date"] = datetime.date.fromisoformat(base["release_date"])
    movie = models.Movie(**base)
    if "actors" in data:
      if len(data) != 3: flask.abort(400)
      actors = utils.validate_data(data["actors"], [int], cast=True)
      movie.actors = actors
    else:
      if len(data) != 2: flask.abort(400)

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

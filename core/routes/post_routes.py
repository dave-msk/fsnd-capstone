from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import logging

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
    route, fn = globals()["make_post_%s" % key]()
    super(PostRoute, self).__init__(route, fn, "POST", permission=permission)


def make_post_actor():
  def post_actor():
    logger = logging.getLogger("Post.Actor")

    data = utils.get_json()
    logger.debug("Input data: {}".format(data))

    spec = {"name": str, "age": int, "gender": str}
    base = utils.validate_data(data, spec, cast=True)
    actor = models.Actor(**base)
    if "movies" in data:
      if len(data) > 4: flask.abort(400)
      movie_ids = utils.validate_data(data["movies"], [int], cast=True)
      movies = [models.Movie.query.get(mid) for mid in movie_ids]
      if any(m is None for m in movies): flask.abort(422)
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
    logger = logging.getLogger("Post.Movie")

    data = utils.get_json()
    logger.debug("Input data: {}".format(data))

    spec = {"title": str, "release_date": str}
    base = utils.validate_data(data, spec, cast=True)
    base["release_date"] = datetime.date.fromisoformat(base["release_date"])
    movie = models.Movie(**base)
    if "actors" in data:
      if len(data) != 3: flask.abort(400)
      actor_ids = utils.validate_data(data["actors"], [int], cast=True)
      actors = [models.Actor.query.get(aid) for aid in actor_ids]
      if any(a is None for a in actors): flask.abort(422)
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

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

    if (any(k not in data for k in {"name", "age", "gender"}) or
        any(k not in {"name", "age", "gender", "movies"} for k in data)):
      flask.abort(400)

    args = {
        "name": utils.validate_and_convert(data["name"], str),
        "age": utils.validate_and_convert(data["age"], int),
        "gender": utils.validate_and_convert(data["gender"], str,
                                             convert_fn=lambda g: g.upper(),
                                             test_fn=models.is_gender,
                                             cast=True),
    }

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
    logger = logging.getLogger("Post.Movie")

    data = utils.get_json()
    logger.debug("Input data: {}".format(data))

    if (any(k not in data for k in {"title", "release_date"}) or
        any(k not in {"title", "release_date", "actors"} for k in data)):
      flask.abort(400)

    args = {
        "title": utils.validate_and_convert(data["title"], str),
        "release_date": utils.validate_and_convert(
            data["release_date"], str,
            convert_fn=lambda s: datetime.datetime.fromisoformat(s)),
    }
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime

import flask

from core import models
from core import utils
from core.routes import routebase


def gather_patch_route_details():
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

  return {"factory": PatchRoute, "sig": sig, "descriptions": desc}


class PatchRoute(routebase.Route):
  def __init__(self, key, permission=None):
    route, fn = globals()["make_patch_%s" % key]()
    super(PatchRoute, self).__init__(route, fn, "PATCH", permission=permission)


def make_patch_actor():
  def patch_actor(actor_id):
    data = utils.get_json()
    actor = models.Actor.query.get(actor_id)
    if actor is None: flask.abort(404)
    if any(k not in {"name", "age", "gender", "movies"} for k in data):
      flask.abort(400)

    try:
      maybe_update_attr(actor, data, "name", str, cast=True)
      maybe_update_attr(actor, data, "age", int, cast=True)
      maybe_update_attr(actor, data, "gender", str,
                        fn=lambda gender: gender.upper(),
                        valid_fn=models.is_gender, cast=True)
      maybe_update_attr(
          actor, data, "movies", [int],
          fn=lambda ids: [models.Movie.query.get(id) for id in ids],
          valid_fn=lambda movies: all(m is not None for m in movies),
          cast=True)
      models.db.session.commit()
    except:
      models.db.session.rollback()
      raise

    return flask.jsonify({
        "success": True,
        "actor": actor.format(),
    })

  return "/actors/<int:actor_id>", patch_actor


def make_patch_movie():
  def patch_movie(movie_id):
    data = utils.get_json()
    movie = models.Movie.query.get(movie_id)
    if movie is None: flask.abort(404)
    if any(k not in {"title", "release_date", "actors"} for k in data):
      flask.abort(400)

    try:
      maybe_update_attr(movie, data, "title", str, cast=True)
      maybe_update_attr(movie, data, "release_date", str,
                        fn=datetime.date.fromisoformat, cast=True)
      maybe_update_attr(
          movie, data, "actors", [int],
          fn=lambda ids: [models.Actor.query.get(id) for id in ids],
          valid_fn=lambda actors: all(a is not None for a in actors),
          cast=True)
      models.db.session.commit()
    except:
      models.db.session.rollback()
      raise

    return flask.jsonify({
        "success": True,
        "movie": movie.format(),
    })

  return "/movies/<int:movie_id>", patch_movie


def maybe_update_attr(record,
                      data,
                      key,
                      dtype,
                      valid_fn=None,
                      fn=None,
                      cast=True):
  if key in data:
    value = utils.validate_data(data[key], dtype, cast=cast)
    if fn:
      try:
        value = fn(value)
      except:
        flask.abort(422)

    if valid_fn and not valid_fn(value):
      flask.abort(422)
    setattr(record, key, value)

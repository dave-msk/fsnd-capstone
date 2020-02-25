from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask

from core import models
from core.routes import routebase


def gather_delete_route_details():
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

  return {"factory": DeleteRoute, "sig": sig, "descriptions": desc}


class DeleteRoute(routebase.Route):
  def __init__(self, key, permission=None):
    super(DeleteRoute, self).__init__(permission=permission)
    self._method = "DELETE"
    self._route, self._fn = globals()["make_delete_%s" % key]()


def make_delete_actor():
  def delete_actor(actor_id):
    actor = models.Actor.query.get(actor_id)
    if actor is None: flask.abort(404)
    try:
      models.db.session.delete(actor)
      models.db.session.commit()
    except:
      models.db.session.rollback()
      raise
    return flask.jsonify({"success": True, "actor_id": actor_id})
  return "/actors/<int:actor_id>", delete_actor


def make_delete_movie():
  def delete_movie(movie_id):
    movie = models.Movie.query.get(movie_id)
    if movie is None: flask.abort(404)
    try:
      models.db.session.delete(movie)
      models.db.session.commit()
    except:
      models.db.session.rollback()
      raise
    return flask.jsonify({"success": True, "movie_id": movie_id})
  return "/movies/<int:movie_id>", delete_movie

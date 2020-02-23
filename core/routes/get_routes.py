from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask

from core import models
from core.routes import routebase


def gather_get_route_details():
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

  return {"factory": GetRoute, "sig": sig, "descriptions": desc}


class GetRoute(routebase.Route):
  def __init__(self, key, permission=None):
    super(GetRoute, self).__init__(permission=permission)
    self._method = "GET"
    self._route, self._fn = globals()["make_get_%s" % key]()


def make_get_actors():
  def get_actors():
    query = models.Actor.query.order_by(models.Actor.id)
    return flask.jsonify({
        "success": True,
        "actors": [a.format() for a in query],
    })
  return "/actors", get_actors


def make_get_movies():
  def get_movies():
    query = models.Movie.query.order_by(models.Movie.id)
    return flask.jsonify({
        "success": True,
        "movies": [m.format() for m in query],
    })
  return "/movies", get_movies
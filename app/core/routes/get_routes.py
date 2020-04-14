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

import flask

from core import models
from core.routes import routebase


def gather_get_route_details():
  desc = {
      "short": "Factory of get-routes for Casting Agency API",
      "long":
          """Creates a GET-route for Casting Agency API.
          
          Available routes:
          
            - actors: GET /actors
            - movies: GET /movies
          """,
  }

  sig = {
      "key": {
          "type": str,
          "description": "Route key, one of [\"actors\", \"movies\"].",
      },
  }
  sig.update(routebase.Route._SIG)  # pylint: disable=protected-access

  return {"factory": GetRoute, "sig": sig, "descriptions": desc}


class GetRoute(routebase.Route):
  def __init__(self, key, permission=None):
    route, fn = globals()["make_get_%s" % key]()
    super(GetRoute, self).__init__(route, fn, "GET", permission=permission)


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

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


def gather_delete_route_details():
  desc = {
      "short": "Factory of DELETE-routes for Casting Agency API",
      "long":
          """Creates a DELETE-route for Casting Agency API.
          
          Available routes:
          
            - actor: DELETE /actors/<int:actor_id>
            - movie: DELETE /movies/<int:movie_id>
          """,
  }

  sig = {
      "key": {
          "type": str,
          "description": "Route key, one of [\"actor\", \"movie\"].",
      },
  }
  sig.update(routebase.Route._SIG)  # pylint: disable=protected-access

  return {"factory": DeleteRoute, "sig": sig, "descriptions": desc}


class DeleteRoute(routebase.Route):
  def __init__(self, key, permission=None):
    route, fn = globals()["make_delete_%s" % key]()
    super(DeleteRoute, self).__init__(route, fn, "DELETE",
                                      permission=permission)


def make_delete_actor():
  def delete_actor(actor_id):
    actor = models.Actor.query.get(actor_id)
    if actor is None: flask.abort(404)  # Ensure existence of specified actor

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
    if movie is None: flask.abort(404)  # Ensure existence of specified movie

    try:
      models.db.session.delete(movie)
      models.db.session.commit()
    except:
      models.db.session.rollback()
      raise
    return flask.jsonify({"success": True, "movie_id": movie_id})
  return "/movies/<int:movie_id>", delete_movie

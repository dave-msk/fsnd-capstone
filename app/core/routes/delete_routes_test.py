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

import unittest
from unittest import mock

from core import configs
from core import models
from core import utils
from core.routes import delete_routes
from core.routes import restful_test_base


class DeleteRoutesURLRuleTestCase(unittest.TestCase):
  def setUp(self):
    self._app = mock.create_autospec(flask.Flask)

  def verify_route(self, route, rule):
    route.apply(self._app)
    route_fn = self._app.route
    route_fn.assert_called_with(rule, methods=["DELETE"])

  def testDeleteActorRule(self):
    route = delete_routes.DeleteRoute("actor")
    self.verify_route(route, "/actors/<int:actor_id>")

  def testDeleteMovieRule(self):
    route = delete_routes.DeleteRoute("movie")
    self.verify_route(route, "/movies/<int:movie_id>")


class DeleteRoutesTestCase(restful_test_base.RestfulRouteTestBase):
  def create_app(self):
    app = utils.create_app_stub(__name__, configs.AppConfig(mode="test"))
    delete_routes.DeleteRoute("actor").apply(app)
    delete_routes.DeleteRoute("movie").apply(app)
    return app

  def testDeleteActor(self):
    actor = models.Actor.query.get(1)
    self.assertIsNotNone(actor)
    expected = {
        "success": True,
        "actor_id": actor.id,
    }
    res = self.client.delete("/actors/1")
    self.compare_json(res, 200, expected)
    actor = models.Actor.query.get(1)
    self.assertIsNone(actor)

  def testDeleteActorNotExist(self):
    res = self.client.delete("/actors/2")
    self.compare_json(res, 404, restful_test_base.ERROR_404)

  def testDeleteMovie(self):
    movie = models.Movie.query.get(1)
    self.assertIsNotNone(movie)
    expected = {
        "success": True,
        "movie_id": movie.id,
    }
    res = self.client.delete("/movies/1")
    self.compare_json(res, 200, expected)
    movie = models.Movie.query.get(1)
    self.assertIsNone(movie)

  def testDeleteMovieNotExist(self):
    res = self.client.delete("/movies/2")
    self.compare_json(res, 404, restful_test_base.ERROR_404)


if __name__ == '__main__':
  unittest.main()

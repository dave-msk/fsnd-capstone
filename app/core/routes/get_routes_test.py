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
from core import utils
from core.routes import get_routes
from core.routes import restful_test_base


class GetRoutesURLRuleTestCase(unittest.TestCase):
  def setUp(self):
    self._app = mock.create_autospec(flask.Flask)

  def verify_route(self, route, rule):
    route.apply(self._app)
    route_fn = self._app.route
    route_fn.assert_called_with(rule, methods=["GET"])

  def testGetActorsRule(self):
    route = get_routes.GetRoute("actors")
    self.verify_route(route, "/actors")

  def testGetMoviesRule(self):
    route = get_routes.GetRoute("movies")
    self.verify_route(route, "/movies")


class GetRoutesTestCase(restful_test_base.RestfulRouteTestBase):
  def create_app(self):
    app = utils.create_app_stub(__name__, configs.AppConfig(mode="test"))
    get_routes.GetRoute("actors").apply(app)
    get_routes.GetRoute("movies").apply(app)
    return app

  def testGetActors(self):
    expected = {
        "success": True,
        "actors": [{"id": 1,
                    "name": "Test Actor",
                    "age": 30,
                    "gender": "F",
                    "movies": [{"id": 1, "title": "Test Movie"}]}],
    }
    res = self.client.get("/actors")
    self.compare_json(res, 200, expected)

  def testGetMovies(self):
    expected = {
        "success": True,
        "movies": [{"id": 1,
                    "title": "Test Movie",
                    "release_date": "1970-01-01",
                    "actors": [{"id": 1, "name": "Test Actor"}]}],
    }
    res = self.client.get("/movies")
    self.compare_json(res, 200, expected)


if __name__ == '__main__':
  unittest.main()

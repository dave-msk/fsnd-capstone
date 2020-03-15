from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask

import unittest
from unittest import mock

from core import configs
from core import models
from core import utils
from core.routes import patch_routes
from core.routes import restful_test_base


class PatchRoutesURLRuleTestCase(unittest.TestCase):
  def setUp(self):
    self._app = mock.create_autospec(flask.Flask)

  def verify_route(self, route, rule):
    route.apply(self._app)
    route_fn = self._app.route
    route_fn.assert_called_with(rule, methods=["PATCH"])

  def testPatchActorRule(self):
    route = patch_routes.PatchRoute("actor")
    self.verify_route(route, "/actors/<int:actor_id>")

  def testPatchMovieRule(self):
    route = patch_routes.PatchRoute("movie")
    self.verify_route(route, "/movies/<int:movie_id>")


class PatchRoutesTestCase(restful_test_base.RestfulRouteTestBase):
  def create_app(self):
    app = utils.create_app_stub(__name__, configs.AppConfig(mode="test"))
    patch_routes.PatchRoute("actor").apply(app)
    patch_routes.PatchRoute("movie").apply(app)
    return app

  def testPatchActorNotExist(self):
    res = self.client.patch("/actors/2", json={})
    self.compare_json(res, 404, restful_test_base.ERROR_404)

  def testPatchActorInvalidInputKey(self):
    res = self.client.patch("/actors/1", json={"invalid_key": "test"})
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  def testPatchActorInvalidAge(self):
    res = self.client.patch("/actors/1", json={"age": "test"})
    self.compare_json(res, 422, restful_test_base.ERROR_422)

  def testPatchActorInvalidGender(self):
    res = self.client.patch("/actors/1", json={"gender": "test"})
    self.compare_json(res, 422, restful_test_base.ERROR_422)

  def testPatchActorInvalidMovies(self):
    res = self.client.patch("/actors/1", json={"movies": "test"})
    self.compare_json(res, 422, restful_test_base.ERROR_422)

  def testPatchActorNonExistMovies(self):
    res = self.client.patch("/actors/1", json={"movies": [1, 2]})
    self.compare_json(res, 422, restful_test_base.ERROR_422)

  def testPatchMovieNotExist(self):
    res = self.client.patch("/movies/2", json={})
    self.compare_json(res, 404, restful_test_base.ERROR_404)

  def testPatchMovieInvalidInputKey(self):
    res = self.client.patch("/movies/1", json={"invalid_key": "test"})
    self.compare_json(res, 400, restful_test_base.ERROR_400)





if __name__ == '__main__':
  unittest.main()

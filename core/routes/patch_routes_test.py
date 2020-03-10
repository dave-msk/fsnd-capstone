from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask

import unittest
from unittest import mock

from core.routes import patch_routes


class GetRoutesTestCase(unittest.TestCase):
  def setUp(self):
    self._app = mock.create_autospec(flask.Flask)

  def verify_route(self, route, rule):
    route.apply(self._app)
    route_fn = self._app.route
    route_fn.assert_called_with(rule, methods=["PATCH"])

  def test_patch_actor(self):
    route = patch_routes.PatchRoute("actor")
    self.verify_route(route, "/actors/<int:actor_id>")

  def test_patch_movie(self):
    route = patch_routes.PatchRoute("movie")
    self.verify_route(route, "/movies/<int:movie_id>")


if __name__ == '__main__':
  unittest.main()

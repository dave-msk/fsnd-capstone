from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask

import unittest
from unittest import mock

from core.routes import get_routes


class GetRoutesTestCase(unittest.TestCase):
  def setUp(self):
    self._app = mock.create_autospec(flask.Flask)

  def verify_route(self, route, rule):
    route.apply(self._app)
    route_fn = self._app.route
    route_fn.assert_called_with(rule, methods=["GET"])

  def test_get_actors(self):
    route = get_routes.GetRoute("actors")
    self.verify_route(route, "/actors")

  def test_get_movies(self):
    route = get_routes.GetRoute("movies")
    self.verify_route(route, "/movies")


if __name__ == '__main__':
  unittest.main()

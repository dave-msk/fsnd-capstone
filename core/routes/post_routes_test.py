from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask

import unittest
from unittest import mock

from core.routes import post_routes


class GetRoutesTestCase(unittest.TestCase):
  def setUp(self):
    self._app = mock.create_autospec(flask.Flask)

  def verify_route(self, route, rule):
    route.apply(self._app)
    route_fn = self._app.route
    route_fn.assert_called_with(rule, methods=["POST"])

  def test_post_actor(self):
    route = post_routes.PostRoute("actor")
    self.verify_route(route, "/actors")

  def test_post_movie(self):
    route = post_routes.PostRoute("movie")
    self.verify_route(route, "/movies")


if __name__ == '__main__':
  unittest.main()

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask

import unittest
from unittest import mock

from core import configs
from core import models
from core import utils
from core.routes import post_routes
from core.routes import restful_test_base


class PostRoutesURLRuleTestCase(unittest.TestCase):
  def setUp(self):
    self._app = mock.create_autospec(flask.Flask)

  def verify_route(self, route, rule):
    route.apply(self._app)
    route_fn = self._app.route
    route_fn.assert_called_with(rule, methods=["POST"])

  def testPostActorRule(self):
    route = post_routes.PostRoute("actor")
    self.verify_route(route, "/actors")

  def testPostMovieRule(self):
    route = post_routes.PostRoute("movie")
    self.verify_route(route, "/movies")


class PostRoutesTestCase(restful_test_base.RestfulRouteTestBase):
  def create_app(self):
    app = utils.create_app_stub(__name__, configs.AppConfig(mode="test"))
    post_routes.PostRoute("actor").apply(app)
    post_routes.PostRoute("movie").apply(app)
    return app

  def testPostActor(self):
    actor = models.Actor(name="Some Actor",
                         )


if __name__ == '__main__':
  unittest.main()

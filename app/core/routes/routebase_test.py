from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask

import unittest
from unittest import mock

from core.routes import routebase


class RouteTestCase(unittest.TestCase):
  def setUp(self):
    self._app = mock.create_autospec(flask.Flask)
    self._fn = mock.Mock(spec=())

  @mock.patch("core.routes.routebase.flask_cors.cross_origin")
  def general_test_apply(self, rule, method, permission, cross_origin):
    route = routebase.Route(rule, self._fn, method, permission=permission)
    ret_fn = route.apply(self._app)

    cross_origin.assert_called_once()

    self._fn.assert_not_called()
    self._app.route.assert_called_once()
    self._app.route.assert_called_with(rule, methods=[method])

    app_route_dec = self._app.route.return_value
    app_route_dec.assert_called_once()
    app_route_ret = app_route_dec.return_value
    self.assertIs(app_route_ret, ret_fn)

  @mock.patch("core.routes.routebase.auth.requires_auth")
  def test_apply_no_permission(self, requires_auth):
    self.general_test_apply("/", "GET", None)
    requires_auth.assert_not_called()

  @mock.patch("core.routes.routebase.auth.requires_auth")
  def test_apply_with_permission(self, requires_auth):
    self.general_test_apply("/some_api", "POST", "post:some_api")
    requires_auth.assert_called_once()
    requires_auth.assert_called_with("post:some_api")


if __name__ == "__main__":
  unittest.main()

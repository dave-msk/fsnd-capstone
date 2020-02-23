from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask_cors as fsk_cors

from core import auth


class Route(object):
  METHODS = {"GET", "HEAD", "POST", "PUT", "DELETE",
             "CONNECT", "OPTION", "TRACE", "PATCH"}

  _SIG = {
      "permission": {
          "type": str,
          "description": "",
      },
  }

  def __init__(self, permission=None):
    # TODO: Validate permission format
    self._permission = permission
    self._route = None
    self._method = None
    self._fn = None

  def _validate_route(self):
    pass

  def _validate_method(self):
    pass

  def _validate_fn(self):
    pass

  def apply(self, app):
    self._validate_route()
    self._validate_method()
    self._validate_fn()

    fn = self._fn()
    if self._permission: fn = auth.requires_auth(self._permission)(fn)
    fn = fsk_cors.cross_origin()(fn)
    fn = app.route(self._route, methods=[self._method])(fn)
    return fn

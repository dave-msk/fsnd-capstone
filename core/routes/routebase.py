from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask_cors

from core import auth


_METHODS = {"GET", "HEAD", "POST", "PUT", "DELETE",
            "CONNECT", "OPTION", "TRACE", "PATCH"}


class Route(object):
  _SIG = {
      "permission": {
          "type": str,
          "description": "",
      },
  }

  def __init__(self, rule, fn, method, permission=None):
    validate_rule(rule)
    validate_fn(fn)
    validate_method(method)
    validate_permission(permission)

    self._rule = rule
    self._fn = fn
    self._method = method
    self._permission = permission

  def apply(self, app):
    fn = self._fn
    if self._permission: fn = auth.requires_auth(self._permission)(fn)
    fn = flask_cors.cross_origin()(fn)
    fn = app.route(self._rule, methods=[self._method])(fn)
    return fn

  def call(self, *args, **kwargs):
    return self._fn(*args, **kwargs)


def validate_rule(route):
  if not isinstance(route, str):
    raise TypeError()
  if not route[0] == "/":
    raise ValueError()


def validate_method(method):
  if not isinstance(method, str):
    raise TypeError()
  if not method in _METHODS:
    raise ValueError()


def validate_fn(fn):
  if not callable(fn):
    raise TypeError()


def validate_permission(permission):
  if permission is None: return
  if not isinstance(permission, str):
    raise TypeError()

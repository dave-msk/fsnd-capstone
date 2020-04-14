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

import flask_cors

from core import auth


_METHODS = {"GET", "HEAD", "POST", "PUT", "DELETE",
            "CONNECT", "OPTION", "TRACE", "PATCH"}


class Route(object):
  _SIG = {
      "permission": {
          "type": str,
          "description": "Permission string. If `None`, public access "
                         "is allowed. Defaults to `None`",
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


def validate_rule(rule):
  if not isinstance(rule, str):
    raise TypeError("`rule` must be a string. Given: {}".format(type(rule)))
  if not rule[0] == "/":
    raise ValueError("`rule` must start with \"/\". Given: \"{}\"".format(rule))


def validate_method(method):
  if method not in _METHODS:
    raise ValueError("`method` must be one of {}. Given: {}"
                     .format(_METHODS, method))


def validate_fn(fn):
  if not callable(fn):
    raise TypeError("`fn` must be callable. Given: {}".format(fn))


def validate_permission(permission):
  if permission is None: return
  if not isinstance(permission, str):
    raise TypeError("`permission` must be a string. Given: {}"
                    .format(type(permission)))

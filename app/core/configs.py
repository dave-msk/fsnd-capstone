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

import os


class AppConfig(object):
  _MODES = {"prod", "dev", "test"}

  def __init__(self, mode=None):
    mode = mode or "prod"
    if mode not in self._MODES:
      raise ValueError("`mode` must be one of [\"prod\", \"dev\", \"test\"]. "
                       "Given: {}".format(mode))

    self.DEBUG = mode == "dev"
    self.TESTING = mode == "test"
    self.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    if mode != "test":
      self.SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]
    self.SQLALCHEMY_TRACK_MODIFICATIONS = mode == "dev"

    def format_permission(p):
      return p if mode == "prod" else None

    routes = None
    if mode != "test":
      routes = [
          {"get": {"key": "actors",
                   "permission": format_permission("get:actors")}},
          {"get": {"key": "movies",
                   "permission": format_permission("get:movies")}},
          {"post": {"key": "actor",
                    "permission": format_permission("post:actors")}},
          {"post": {"key": "movie",
                    "permission": format_permission("post:movies")}},
          {"patch": {"key": "actor",
                     "permission": format_permission("patch:actors")}},
          {"patch": {"key": "movie",
                     "permission": format_permission("patch:movies")}},
          {"delete": {"key": "actor",
                      "permission": format_permission("delete:actors")}},
          {"delete": {"key": "movie",
                      "permission": format_permission("delete:movies")}},
      ]

    self.ROUTES = routes

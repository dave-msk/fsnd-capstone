from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os


class AppConfig(object):
  _MODES = {"prod", "dev", "test"}

  def __init__(self, mode=None):
    mode = mode or "prod"
    if mode not in self._MODES:
      raise ValueError()

    self.DEBUG = mode == "dev"
    self.TESTING = mode == "test"
    self.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    if mode == "prod":
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class Config(object):
  DEBUG = False
  TESTING = False
  SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  ROUTES = [
      {"get": {"key": "actors", "permission": "get:actors"}},
      {"get": {"key": "movies", "permission": "get:movies"}},
      {"post": {"key": "actor", "permission": "post:actors"}},
      {"post": {"key": "movie", "permission": "post:movies"}},
      {"patch": {"key": "actor", "permission": "patch:actors"}},
      {"patch": {"key": "movie", "permission": "patch:movies"}},
      {"delete": {"key": "actor", "permission": "delete:actors"}},
      {"delete": {"key": "movie", "permission": "delete:movies"}},
  ]


class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = "postgresql://david:sqlDev@localhost:5432/fscpst"


class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
  TESTING = True

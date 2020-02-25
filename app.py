from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import yaml
import flask as fsk
import flask_migrate as fsk_mgt
import flask_moment as fsk_mmt
import flask_cors as fsk_cors

from core import errors
from core import models
from core.routes import registry
from core.routes import routebase


def load_routes_config(path=None):
  if path is None:
    path = os.path.join(os.path.dirname(__file__), "routes.yaml")
  with open(path, "r") as fin:
    return yaml.load(fin)


def create_app(test_config=None, database_path=None, routes_path=None):
  # create and configure the app
  app = fsk.Flask(__name__)
  fsk_mmt.Moment(app)

  if database_path is None: database_path = os.environ["DATABASE_URL"]
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  models.db.init_app(app)

  fsk_mgt.Migrate(app, models.db)
  fsk_cors.CORS(app)

  # TODO: Register error handlers
  errors.add_error(app, 400, "bad request")
  errors.add_error(app, 404, "resource not found")
  errors.add_error(app, 422, "unprocessable")
  errors.add_auth_error(app)

  # TODO: Register routes
  routes_config = load_routes_config(
      routes_path if routes_path is not None else os.environ.get("ROUTES"))
  broker = registry.make_broker()
  routes = [broker.make(routebase.Route, spec) for spec in routes_config]
  [r.apply(app) for r in routes]

  return app


if __name__ == "__main__":
  app = create_app()
  app.run(host="0.0.0.0", port=8080, debug=True)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import logging

import yaml
import flask as fsk
import flask_migrate as fsk_mgt
import flask_moment as fsk_mmt
import flask_cors as fsk_cors

from core import configs
from core import errors
from core import models
from core.routes import registry
from core.routes import routebase


def create_app(config=None):
  # create and configure the app
  app = fsk.Flask(__name__)
  fsk_mmt.Moment(app)

  config = config or configs.ProductionConfig()
  app.config.from_object(config)
  models.db.init_app(app)

  fsk_mgt.Migrate(app, models.db)
  fsk_cors.CORS(app)

  # Register error handlers
  errors.add_error(app, 400, "bad request")
  errors.add_error(app, 404, "resource not found")
  errors.add_error(app, 422, "unprocessable")
  errors.add_auth_error(app)

  # Register routes
  broker = registry.make_broker()
  routes = [broker.make(routebase.Route, spec) for spec in app.config["ROUTES"]]
  [r.apply(app) for r in routes]

  return app


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  app = create_app()
  app.run(host="0.0.0.0", port=8080, debug=True)

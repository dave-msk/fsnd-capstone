from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from core import configs
from core import utils
from core.routes import registry
from core.routes import routebase


def create_app(config=None):
  # create and configure the app
  config = config or configs.AppConfig()
  app = utils.create_app_stub(__name__, config)

  # Register routes
  broker = registry.make_broker()
  routes = [broker.make(routebase.Route, spec) for spec in app.config["ROUTES"]]
  [r.apply(app) for r in routes]

  return app


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  app = create_app()
  app.run(host="0.0.0.0", port=8080, debug=True)

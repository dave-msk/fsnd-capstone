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

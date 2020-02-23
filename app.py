from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import flask as fsk
import flask_migrate as fsk_mgt
import flask_moment as fsk_mmt
import flask_cors as fsk_cors

from core import models


def create_app(test_config=None, database_path=None):
  # create and configure the app
  app = fsk.Flask(__name__)
  fsk_mmt.Moment(app)

  if database_path is None: database_path = os.environ["DATABASE_URL"]
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  models.db.init_app(app)

  fsk_mgt.Migrate(app, models.db)
  fsk_cors.CORS(app)

  # TODO: Register routes

  return app


if __name__ == "__main__":
  app = create_app()
  app.run(host="0.0.0.0", port=8080, debug=True)

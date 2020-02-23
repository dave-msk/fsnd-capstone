from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import flask as fsk
import flask_migrate as fsk_mgt
import flask_moment as fsk_mmt
import flask_cors as fsk_cors

import models


def create_app(test_config=None):
  # create and configure the app
  app = fsk.Flask(__name__)
  fsk_mmt.Moment(app)
  db, m = models.setup_db(app)
  fsk_mgt.Migrate(app, db)
  fsk_cors.CORS(app)

  return app


if __name__ == "__main__":
  app = create_app()
  app.run(host="0.0.0.0", port=8080, debug=True)

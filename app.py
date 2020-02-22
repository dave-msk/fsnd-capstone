from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import flask as fsk
import flask_sqlalchemy as fsk_sa
import flask_cors as fsk_cors


def create_app(test_config=None):
  # create and configure the app
  app = fsk.Flask(__name__)
  fsk_cors.CORS(app)

  return app

APP = create_app()

if __name__ == '__main__':
  APP.run(host='0.0.0.0', port=8080, debug=True)

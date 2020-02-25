from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask

from core import auth


def add_error(app, code, message):
  @app.errorhandler(code)
  def handler(error):
    res = flask.jsonify({
        "success": False,
        "error": code,
        "message": message,
    })
    return res, code


def add_auth_error(app):
  @app.errorhandler(auth.AuthError)
  def handler(error):
    res = flask.jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error["description"],
    })
    return res, error.status_code

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask
import flask_migrate
import flask_moment
import flask_cors

from core import errors
from core import models


def create_app_stub(import_name, config):
  # create and configure app
  app = flask.Flask(import_name)
  app.config.from_object(config)

  flask_moment.Moment(app)
  models.db.init_app(app)
  flask_migrate.Migrate(app, models.db)
  flask_cors.CORS(app)

  # Register error handlers
  errors.add_error(app, 400, "bad request")
  errors.add_error(app, 404, "resource not found")
  errors.add_error(app, 422, "unprocessable")
  errors.add_auth_error(app)

  return app


def get_json():
  if not flask.request.is_json: flask.abort(400)
  return flask.request.get_json()


def validate_and_convert(data, dtype, convert_fn=None, test_fn=None, cast=True):
  value = validate_dtype(data, dtype, cast=cast)
  if convert_fn:
    try:
      value = convert_fn(value)
    except:
      flask.abort(422)

  if test_fn and not test_fn(value): flask.abort(422)
  return value


def validate_dtype(data, dtype, cast=True):
  if isinstance(dtype, type):
    if cast:
      try:
        data = dtype(data)
      except:
        flask.abort(400)
    elif not isinstance(dtype, type):
      flask.abort(400)
    return data

  if isinstance(dtype, list):
    if len(dtype) != 1:
      raise ValueError()
    if not isinstance(data, (list, tuple)): flask.abort(400)
    return [validate_dtype(d, dtype[0], cast=cast) for d in data]

  if isinstance(dtype, tuple):
    if not isinstance(data, (list, tuple)) or len(data) != len(dtype):
      flask.abort(400)
    return tuple(validate_dtype(d, s, cast=cast) for d, s in zip(data, dtype))

  if isinstance(dtype, dict):
    if not all(isinstance(k, str) for k in dtype):
      raise ValueError()

    if not isinstance(data, dict) or not set(dtype).issubset(set(data)):
      flask.abort(400)
    return {k: validate_dtype(data[k], s, cast=cast)
            for k, s in dtype.items()}

  raise TypeError()

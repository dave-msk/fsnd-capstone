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
  errors.add_error(app, 500, "server error")
  errors.add_auth_error(app)

  return app


def get_json():
  if not flask.request.is_json: flask.abort(400)
  return flask.request.get_json()


def validate_and_convert(data, dtype, convert_fn=None, test_fn=None, cast=True):
  """Validate data type and perform conversion.

  Args:
    data: Object to be validated and converted (if applicable)
    dtype: Expected type of `data`
    convert_fn: (Optional) Function that converts `data` after type validation.
    test_fn: (Optional) Function that validates the converted result.
    cast: Cast `data` to type `dtype` instead of checking if `data` is of
      type `dtype`. Defaults to True.

  Returns:
    Final output from casting (if applicable) followed by
    conversion (if applicable).
  """
  value = validate_dtype(data, dtype, cast=cast)
  if convert_fn:
    try:
      value = convert_fn(value)
    except:
      flask.abort(422)

  if test_fn and not test_fn(value): flask.abort(422)
  return value


def validate_dtype(data, dtype, cast=True):
  """Validate if data conforms to the given structure.
  """
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
      raise ValueError("`dtype` must be a single when it is a list. Length: {}"
                       .format(len(dtype)))
    if not isinstance(data, (list, tuple)): flask.abort(400)
    return [validate_dtype(d, dtype[0], cast=cast) for d in data]

  if isinstance(dtype, tuple):
    if not isinstance(data, (list, tuple)) or len(data) != len(dtype):
      flask.abort(400)
    return tuple(validate_dtype(d, s, cast=cast) for d, s in zip(data, dtype))

  if isinstance(dtype, dict):
    if not all(isinstance(k, str) for k in dtype):
      raise ValueError("`dtype` must be string-keyed. Given: {}".format(dtype))

    if not isinstance(data, dict) or not set(dtype).issubset(set(data)):
      flask.abort(400)
    return {k: validate_dtype(data[k], s, cast=cast)
            for k, s in dtype.items()}

  raise TypeError("`dtype` must either be a type, list, tuple or dict. "
                  "Given: {}".format(type(dtype)))

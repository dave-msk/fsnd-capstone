from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask


def get_json():
  if not flask.request.is_json: flask.abort(400)
  return flask.request.get_json()


def validate_data(data, spec, cast=True):
  if isinstance(spec, type):
    if cast:
      try:
        data = spec(data)
      except:
        flask.abort(400)
    elif not isinstance(spec, type):
      flask.abort(400)
    return data

  if isinstance(spec, list):
    if len(spec) != 1:
      raise ValueError()
    if not isinstance(data, (list, tuple)): flask.abort(400)
    return [validate_data(d, spec[0], cast=cast) for d in data]

  if isinstance(spec, tuple):
    if not isinstance(data, (list, tuple)) or len(data) != len(spec):
      flask.abort(400)
    return tuple(validate_data(d, s, cast=cast) for d, s in zip(data, spec))

  if isinstance(spec, dict):
    if not all(isinstance(k, str) for k in spec):
      raise ValueError()

    if not isinstance(data, dict) or not set(spec).issubset(set(data)):
      flask.abort(400)
    return {k: validate_data(data[k], s, cast=cast)
            for k, s in spec.items()}

  raise TypeError()

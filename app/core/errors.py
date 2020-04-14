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

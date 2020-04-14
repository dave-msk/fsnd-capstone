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

import datetime
import itertools

import flask_testing
from absl.testing import parameterized

from core import models

ERROR_400 = {"success": False, "error": 400, "message": "bad request"}
ERROR_404 = {"success": False, "error": 404, "message": "resource not found"}
ERROR_422 = {"success": False, "error": 422, "message": "unprocessable"}
ERROR_500 = {"success": False, "error": 500, "message": "server error"}


class RestfulRouteTestBase(flask_testing.TestCase):
  def setUp(self):
    models.db.create_all()
    test_actor = models.Actor(id=1,
                              name="Test Actor",
                              age=30,
                              gender="F")
    test_movie = models.Movie(id=1,
                              title="Test Movie",
                              release_date=datetime.date(1970, 1, 1),
                              actors=[test_actor])
    models.db.session.add(test_actor)
    models.db.session.add(test_movie)
    models.db.session.commit()
    models.db.session.close()

  def tearDown(self):
    models.db.session.remove()
    models.db.drop_all()

  def compare_json(self, res, code, expected):
    self.assertEqual(res.status_code, code)
    self.assertTrue(res.is_json)
    self.assertDictEqual(res.json, expected)


def generate(**kwargs):
  def decorator(test_method):
    keys = sorted(kwargs)
    combinations = [dict(zip(keys, p)) for p in itertools.product(
        *[kwargs[k]for k in keys])]

    return parameterized.parameters(*combinations)(test_method)

  return decorator

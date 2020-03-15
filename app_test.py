from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime

from unittest import mock

import flask_testing
from absl.testing import parameterized

import app
from core import configs
from core import models


ERROR_400 = {"success": False, "error": 400, "message": "bad request"}
ERROR_404 = {"success": False, "error": 404, "message": "resource not found"}
ERROR_422 = {"success": False, "error": 422, "message": "unprocessable"}
ERROR_500 = {"success": False, "error": 500, "message": "server error"}


_PERMISSIONS = {"get:actors", "get:movies",
                "post:actors", "post:movies",
                "patch:actors", "patch:movies",
                "delete:actors", "delete:movies"}


def generate_unauthorized(endpoint_method_permission_tuples):
  params = []
  for endpoint, method, permission in endpoint_method_permission_tuples:
    params.extend({"endpoint": endpoint, "method": method, "permission": p}
                  for p in _PERMISSIONS if p != permission)

  def decorator(test_method):
    return parameterized.named_parameters(*params)(test_method)

  return decorator


class CastingAgencyAPITestCase(flask_testing.TestCase):
  def create_app(self):
    return app.create_app(configs.AppConfig(mode="test"))

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

  @mock.patch("core.auth.verify_decode_jwt")
  def call_with_permission(self,
                           endpoint,
                           method,
                           permissions,
                           verify_decode_jwt):
    verify_decode_jwt.return_value = {"permissions": permissions}
    header = {"Authorization": "Bearer JWT_Token"}



  def testUnauthorizedAccess(self, endpoint, method, permission):
    pass


class CastingAgencyAPIUnauthorizedTestCase(
    flask_testing.TestCase, parameterized.TestCase):
  def create_app(self):
    return app.create_app(configs.AppConfig(mode="test"))

  def setUp(self):
    models.db.create_all()

  def tearDown(self):
    models.db.session.remove()
    models.db.drop_all()

  def assert_unauthorized(self, res):
    self.assertEqual(res.status_code, 401)
    self.assertTrue(res.is_json)
    data = res.json
    self.assertEqual(data["success"], False)
    self.assertEqual(data["code"], 401)

  def test_get_actors_unauthorized(self):
    res = self.client.get("/actors")
    self.assert_unauthorized(res)

  def test_get_movies_unauthorized(self):
    res = self.client.get("/movies")
    self.assert_unauthorized(res)

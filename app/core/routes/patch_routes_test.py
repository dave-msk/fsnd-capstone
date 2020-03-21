from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask
from absl.testing import parameterized

import unittest
from unittest import mock

from core import configs
from core import models
from core import utils
from core.routes import patch_routes
from core.routes import restful_test_base


class PatchRoutesURLRuleTestCase(unittest.TestCase):
  def setUp(self):
    self._app = mock.create_autospec(flask.Flask)

  def verify_route(self, route, rule):
    route.apply(self._app)
    route_fn = self._app.route
    route_fn.assert_called_with(rule, methods=["PATCH"])

  def testPatchActorRule(self):
    route = patch_routes.PatchRoute("actor")
    self.verify_route(route, "/actors/<int:actor_id>")

  def testPatchMovieRule(self):
    route = patch_routes.PatchRoute("movie")
    self.verify_route(route, "/movies/<int:movie_id>")


class PatchRoutesTestCase(
    restful_test_base.RestfulRouteTestBase, parameterized.TestCase):
  def create_app(self):
    app = utils.create_app_stub(__name__, configs.AppConfig(mode="test"))
    patch_routes.PatchRoute("actor").apply(app)
    patch_routes.PatchRoute("movie").apply(app)
    return app

  @restful_test_base.generate(name=[None, "Test Patch Actor"],
                              age=[None, 10, 30, 60],
                              gender=[None, "M", "F"],
                              movies=[None, [1]])
  def testPatchActor(self, name=None, age=None, gender=None, movies=None):
    actor = models.Actor.query.get(1)
    data = {}
    if name:
      data["name"] = name
    else:
      name = actor.name

    if age:
      data["age"] = age
    else:
      age = actor.age

    if gender:
      data["gender"] = gender
    else:
      gender = actor.gender

    if movies:
      data["movies"] = movies
      movies = [models.Movie.query.get(mid) for mid in movies]
      movies = sorted(({"id": m.id, "title": m.title} for m in movies),
                      key=lambda d: d["id"])
    else:
      movies = sorted(({"id": m.id, "title": m.title} for m in actor.movies),
                      key=lambda d: d["id"])

    res = self.client.patch("/actors/1", json=data)
    self.assertEqual(res.status_code, 200)
    self.assertTrue(res.is_json)
    res_data = res.json

    self.assertEqual(res_data["success"], True)

    res_actor = res_data["actor"]
    self.assertEqual(res_actor["name"], name)
    self.assertEqual(res_actor["age"], age)
    self.assertEqual(res_actor["gender"], gender)
    self.assertListEqual(
        sorted(res_actor["movies"], key=lambda d: d["id"]), movies)

  def testPatchActorNotExist(self):
    res = self.client.patch("/actors/2", json={})
    self.compare_json(res, 404, restful_test_base.ERROR_404)

  def testPatchActorInvalidInputKey(self):
    res = self.client.patch("/actors/1", json={"invalid": "invalid"})
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  def testPatchActorInvalidAge(self):
    res = self.client.patch("/actors/1", json={"age": "invalid"})
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  def testPatchActorInvalidGender(self):
    res = self.client.patch("/actors/1", json={"gender": "invalid"})
    self.compare_json(res, 422, restful_test_base.ERROR_422)

  def testPatchActorInvalidMovies(self):
    res = self.client.patch("/actors/1", json={"movies": "invalid"})
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  def testPatchActorNonExistMovies(self):
    res = self.client.patch("/actors/1", json={"movies": [2]})
    self.compare_json(res, 422, restful_test_base.ERROR_422)

  @restful_test_base.generate(title=[None, "Test Patch Title"],
                              release_date=[None, "1970-01-01", "2019-07-21"],
                              actors=[None, [1]])
  def testPatchMovie(self, title=None, release_date=None, actors=None):
    movie = models.Movie.query.get(1)
    data = {}

    if title:
      data["title"] = title
    else:
      title = movie.title

    if release_date:
      data["release_date"] = release_date
    else:
      release_date = movie.release_date.isoformat()

    if actors:
      data["actors"] = actors
      actors = [models.Actor.query.get(aid) for aid in actors]
      actors = sorted(({"id": a.id, "name": a.name} for a in actors),
                      key=lambda d: d["id"])
    else:
      actors = sorted(({"id": a.id, "name": a.name} for a in movie.actors),
                      key=lambda d: d["id"])

    res = self.client.patch("/movies/1", json=data)
    self.assertEqual(res.status_code, 200)
    self.assertTrue(res.is_json)
    res_data = res.json

    self.assertEqual(res_data["success"], True)

    res_movie = res_data["movie"]
    self.assertEqual(res_movie["title"], title)
    self.assertEqual(res_movie["release_date"], release_date)
    self.assertListEqual(
        sorted(res_movie["actors"], key=lambda d: d["id"]), actors)

  def testPatchMovieNotExist(self):
    res = self.client.patch("/movies/2", json={})
    self.compare_json(res, 404, restful_test_base.ERROR_404)

  def testPatchMovieInvalidInputKey(self):
    res = self.client.patch("/movies/1", json={"invalid": "invalid"})
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  def testPatchMovieInvalidReleaseDate(self):
    res = self.client.patch("/movies/1", json={"release_date": "invalid"})
    self.compare_json(res, 422, restful_test_base.ERROR_422)

  def testPatchMovieInvalidActors(self):
    res = self.client.patch("/movies/1", json={"actors": "invalid"})
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  def testPatchMovieNonExistActors(self):
    res = self.client.patch("/movies/1", json={"actors": [2]})
    self.compare_json(res, 422, restful_test_base.ERROR_422)


if __name__ == '__main__':
  unittest.main()

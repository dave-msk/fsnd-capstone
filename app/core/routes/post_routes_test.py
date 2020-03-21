from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest
from unittest import mock

import flask
from absl.testing import parameterized

from core import configs
from core import models
from core import utils
from core.routes import post_routes
from core.routes import restful_test_base


class PostRoutesURLRuleTestCase(unittest.TestCase):
  def setUp(self):
    self._app = mock.create_autospec(flask.Flask)

  def verify_route(self, route, rule):
    route.apply(self._app)
    route_fn = self._app.route
    route_fn.assert_called_with(rule, methods=["POST"])

  def testPostActorRule(self):
    route = post_routes.PostRoute("actor")
    self.verify_route(route, "/actors")

  def testPostMovieRule(self):
    route = post_routes.PostRoute("movie")
    self.verify_route(route, "/movies")


class PostRoutesTestCase(
    restful_test_base.RestfulRouteTestBase, parameterized.TestCase):
  def create_app(self):
    app = utils.create_app_stub(__name__, configs.AppConfig(mode="test"))
    post_routes.PostRoute("actor").apply(app)
    post_routes.PostRoute("movie").apply(app)
    return app

  @restful_test_base.generate(name=["Actor 1", "Actor 2"],
                              age=[10, 30, 60],
                              gender=["M", "F"],
                              movie_ids=[None, [1]])
  def testPostActor(self, name, age, gender, movie_ids=None):
    data = {"name": name, "age": age, "gender": gender}
    if movie_ids:
      movie_ids.sort()
      data["movies"] = movie_ids
      movies = [models.Movie.query.get(mid) for mid in movie_ids]
      movies_metadata = [{"id": m.id, "title": m.title} for m in movies]
    else:
      movie_ids, movies_metadata = [], []

    res = self.client.post("/actors", json=data)
    self.assertEqual(res.status_code, 200)
    self.assertTrue(res.is_json)
    res_data = res.json

    self.assertEqual(res_data["success"], True)

    res_actor = res_data["actor"]
    self.assertEqual(res_actor["name"], name)
    self.assertEqual(res_actor["age"], age)
    self.assertEqual(res_actor["gender"], gender)
    self.assertListEqual(
        sorted(res_actor["movies"], key=lambda d: d["id"]), movies_metadata)

    self.assertIsInstance(res_actor["id"], int)

    aid = res_actor["id"]
    actor = models.Actor.query.get(aid)
    self.assertEqual(actor.name, name)
    self.assertEqual(actor.age, age)
    self.assertEqual(actor.gender, gender)
    self.assertListEqual(sorted(m.id for m in actor.movies), movie_ids)

  def testPostActorEmptyInput(self):
    res = self.client.post("/actors", json={})
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  @restful_test_base.generate(key=["name", "age", "gender"])
  def testPostActorMissingRequiredInput(self, key):
    inputs = {
        "name": "name",
        "age": 24,
        "gender": "M",
    }
    inputs.pop(key)
    res = self.client.post("/actors", json=inputs)
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  def testPostActorInvalidInputKey(self):
    res = self.client.post("/actors", json={"invalid": "invalid"})
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  def testPostActorInvalidAge(self):
    res = self.client.post(
        "/actors", json={"name": "name", "age": "invalid", "gender": "F"})
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  def testPostActorInvalidGender(self):
    res = self.client.post(
        "/actors", json={"name": "name", "age": 24, "gender": "invalid"})
    self.compare_json(res, 422, restful_test_base.ERROR_422)

  def testPostActorInvalidMovies(self):
    inputs = {
        "name": "Name",
        "age": 24,
        "gender": "F",
        "movies": "invalid",
    }
    res = self.client.post("/actors", json=inputs)
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  def testPostActorNonExistMovies(self):
    inputs = {
        "name": "Name",
        "age": 24,
        "gender": "F",
        "movies": [2, 3],
    }
    res = self.client.post("/actors", json=inputs)
    self.compare_json(res, 422, restful_test_base.ERROR_422)

  @restful_test_base.generate(title=["Test Movie 1", "Test Movie 2"],
                              release_date=["2019-06-12", "2019-08-31"],
                              actor_ids=[None, [1]])
  def testPostMovie(self, title, release_date, actor_ids=None):
    data = {"title": title, "release_date": release_date}
    if actor_ids:
      actor_ids.sort()
      data["actors"] = actor_ids
      actors = [models.Actor.query.get(aid) for aid in actor_ids]
      actors_metadata = [{"id": a.id, "name": a.name} for a in actors]
    else:
      actor_ids, actors_metadata = [], []

    res = self.client.post("/movies", json=data)
    self.assertEqual(res.status_code, 200)
    self.assertTrue(res.is_json)
    res_data = res.json

    self.assertEqual(res_data["success"], True)

    res_movie = res_data["movie"]
    self.assertEqual(res_movie["title"], title)
    self.assertEqual(res_movie["release_date"], release_date)
    self.assertListEqual(
        sorted(res_movie["actors"], key=lambda d: d["id"]), actors_metadata)

    self.assertIsInstance(res_movie["id"], int)

    mid = res_movie["id"]
    movie = models.Movie.query.get(mid)
    self.assertEqual(movie.title, title)
    self.assertEqual(movie.release_date.isoformat(), release_date)
    self.assertListEqual(sorted(a.id for a in movie.actors), actor_ids)

  def testPostMovieEmptyInput(self):
    res = self.client.post("/movies", json={})
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  @restful_test_base.generate(key=["title", "release_date"])
  def testPostMovieMissingRequiredInput(self, key):
    inputs = {
        "title": "title",
        "release_date": "2019-07-21",
    }
    inputs.pop(key)
    res = self.client.post("/movies", json=inputs)
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  def testPostMovieInvalidReleaseDate(self):
    res = self.client.post("/movies", json={"title": "title",
                                            "release_date": "invalid"})
    self.compare_json(res, 422, restful_test_base.ERROR_422)

  def testPostMovieInvalidActors(self):
    inputs = {
        "title": "Prince Edwards",
        "release_date": "2019-08-31",
        "actors": "Innocent citizens",
    }
    res = self.client.post("/movies", json=inputs)
    self.compare_json(res, 400, restful_test_base.ERROR_400)

  def testPostMovieNonExistActors(self):
    inputs = {
        "title": "North West",
        "release_date": "2019-07-21",
        "actors": [2, 3],
    }
    res = self.client.post("/movies", json=inputs)
    self.compare_json(res, 422, restful_test_base.ERROR_422)


if __name__ == '__main__':
  unittest.main()

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import unittest

from core import models


class MovieTestCase(unittest.TestCase):
  def test_format_without_actors(self):
    movie = models.Movie(id=6,
                         title="Test Movie Without Actors",
                         release_date=datetime.date(2019, 6, 12))
    self.assertDictEqual(movie.format(),
                         {"id": 6,
                          "title": "Test Movie Without Actors",
                          "release_date": "2019-06-12",
                          "actors": []})

  def test_format_with_actors(self):
    actor = models.Actor(id=65, name="Test Actor", age=30, gender="M")
    movie = models.Movie(id=64,
                         title="Test Movie With Actors",
                         release_date=datetime.date(2019, 7, 21),
                         actors=[actor])
    self.assertDictEqual(movie.format(),
                         {"id": 64,
                          "title": "Test Movie With Actors",
                          "release_date": "2019-07-21",
                          "actors": [{"id": 65, "name": "Test Actor"}]})


class ActorTestCase(unittest.TestCase):
  def test_format_without_movies(self):
    actor = models.Actor(id=93,
                         name="Test Actor Without Movies",
                         age=30,
                         gender="M")
    self.assertDictEqual(actor.format(),
                         {"id": 93,
                          "name": "Test Actor Without Movies",
                          "age": 30,
                          "gender": "M",
                          "movies": []})

  def test_format_with_movies(self):
    movie = models.Movie(id=62,
                         title="Test Movie",
                         release_date=datetime.date(2019, 8, 31))
    actor = models.Actor(id=9,
                         name="Test Actor With Movies",
                         age=30,
                         gender="M",
                         movies=[movie])
    self.assertDictEqual(actor.format(),
                         {"id": 9,
                          "name": "Test Actor With Movies",
                          "age": 30,
                          "gender": "M",
                          "movies": [{"id": 62, "title": "Test Movie"}]})


if __name__ == '__main__':
  unittest.main()

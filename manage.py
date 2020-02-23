from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import flask_migrate as fsk_mgt
import flask_script as fsk_s

import app


def create_manager():
  manager = fsk_s.Manager(app.create_app())
  manager.add_command("db", fsk_mgt.MigrateCommand)
  return manager


if __name__ == "__main__":
  manager = create_manager()
  manager.run()

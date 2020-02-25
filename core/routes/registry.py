from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import afb

from core.routes import delete_routes
from core.routes import get_routes
from core.routes import patch_routes
from core.routes import post_routes
from core.routes import routebase


def make_broker():
  details_fns = {
      "delete": delete_routes.gather_delete_route_details,
      "get": get_routes.gather_get_route_details,
      "patch": patch_routes.gather_patch_route_details,
      "post": post_routes.gather_post_route_details,
  }

  broker = afb.Broker()
  broker.register(
      afb.create_mfr(routebase.Route, details_fns, keyword_mode=True))
  return broker

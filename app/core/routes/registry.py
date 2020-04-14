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

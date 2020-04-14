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

from core.routes.routebase import Route
from core.routes.delete_routes import DeleteRoute
from core.routes.get_routes import GetRoute
from core.routes.patch_routes import PatchRoute
from core.routes.post_routes import PostRoute

from core.routes.delete_routes import gather_delete_route_details
from core.routes.get_routes import gather_get_route_details
from core.routes.patch_routes import gather_patch_route_details
from core.routes.post_routes import gather_post_route_details

from core.routes import registry

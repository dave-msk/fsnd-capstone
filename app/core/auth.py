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

import functools
import json
from urllib import request as urlreq

import flask
from jose import jwt

AUTH0_DOMAIN = "dmskdev.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "Casting Agency"


# AuthError Exception
class AuthError(Exception):
  """
  AuthError Exception
  A standardized way to communicate auth failure modes
  """

  def __init__(self, error, status_code):
    self.error = error
    self.status_code = status_code


# Auth Header
def get_token_auth_header():
  """Get the authorization header from the request.

  Returns:
    The token part of the authorization header.

  Raises:
    AuthError:
      - If no header is present
      - If the header is malformed
  """
  auth = flask.request.headers.get("Authorization", None)
  if auth is None:
    raise AuthError({
      "code": "authorization_header_missing",
      "description": "Authorization header is expected.",
    }, 401)

  parts = auth.split(" ")
  if parts[0].lower() != "bearer":
    raise AuthError({
      "code": "invalid_header",
      "description": "Authorization header must start with \"Bearer\"."
    }, 401)
  elif len(parts) == 1:
    raise AuthError({
      "code": "invalid_header",
      "description": "Token not found.",
    }, 401)
  elif len(parts) > 2:
    raise AuthError({
      "code": "invalid_header",
      "description": "Authorization header must be bearer token.",
    }, 401)

  return parts[1]


def check_permissions(permission, payload):
  """Checks if the payload has the required permission.

  Args:
    permission: string permission (i.e. "post:drink")
    payload: decoded jwt payload

  Returns:
    True

  Raises:
    AuthError:
      - If payload does not contain "permissions"
      - If the requested permission string is not in the payload
        permission array
  """
  permissions = payload.get("permissions")
  if permissions is None:
    raise AuthError({
      "code": "invalid_claims",
      "description": "Permissions not included in JWT.",
    }, 400)

  if permission not in permissions:
    raise AuthError({
      "code": "unauthorized",
      "description": "Operation not permitted.",
    }, 401)

  return True


def verify_decode_jwt(token):
  """Verify and decode JWT token.

  The given token should be an Auth0 token with key id (kid).

  Args:
    token: a json web token (string)

  Returns:
    The decoded payload

  Raises:
  AuthError:
    - If "kid" is not in the token header
    - If the token is expired
    - If the claim is invalid
    - If the token is not parsable
    - If the RSA key is not found
  """
  jsonurl = urlreq.urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
  jwks = json.loads(jsonurl.read())
  unverified_header = jwt.get_unverified_header(token)
  rsa_key = {}

  if "kid" not in unverified_header:
    raise AuthError({
      "code": "invalid_header",
      "description": "Authorization malformed.",
    }, 401)
  kid = unverified_header["kid"]

  for key in jwks["keys"]:
    if key["kid"] == kid:
      rsa_key = {k: key[k] for k in ("kty", "kid", "use", "n", "e")}
      break

  if rsa_key:
    try:
      payload = jwt.decode(token,
                           rsa_key,
                           algorithms=ALGORITHMS,
                           audience=API_AUDIENCE,
                           issuer=f"https://{AUTH0_DOMAIN}/")
      return payload

    except jwt.ExpiredSignatureError:
      raise AuthError({
        "code": "token_expired",
        "description": "Token expired.",
      }, 401)

    except jwt.JWTClaimsError:
      raise AuthError({
        "code": "invalid_claims",
        "description": "Incorrect claims. "
                       "Please, check the audience and issuer.",
      }, 401)

    except Exception:
      raise AuthError({
        "code": "invalid_header",
        "description": "Unable to parse authentication token.",
      }, 400)
  raise AuthError({
    "code": "invalid_header",
    "description": "Unable to find the appropriate key.",
  }, 400)


def requires_auth(permission=""):
  """Adds authorization requirement to an endpoint function.

  Args:
    permission: string permission (e.g. "post:drink")

  Returns:
    Decorator with passes the decoded payload to the decorated method
  """

  def requires_auth_decorator(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
      token = get_token_auth_header()
      payload = verify_decode_jwt(token)
      check_permissions(permission, payload)
      return f(*args, **kwargs)

    return wrapper

  return requires_auth_decorator

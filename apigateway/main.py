import base64
import json

from flask import Flask, request, make_response
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["OPTIONS"])
@app.route("/getUser", methods=["OPTIONS"])
def preflight():
    # Return a 200 response with CORS headers set for preflight OPTIONS requests
    return _set_cors_headers(make_response())

@app.route("/", methods=["GET"])
@app.route("/getUser", methods=["GET"])
def hello():
    try:
        id_info = _get_verified_user_info()
    except (ValueError, json.JSONDecodeError) as err:
        return _set_cors_headers(make_response(str(err), 401))

    # Return a message including the name claim of the token
    resp = make_response(f"Welcome {id_info['name']}")
    return _set_cors_headers(resp)

def _get_verified_user_info():
    # API Gateway verifies the token and forwards the payload in this header.
    encoded_info = request.headers.get("X-Apigateway-Api-Userinfo")

    if encoded_info:
        padded_info = encoded_info + "=" * (-len(encoded_info) % 4)
        decoded_info = base64.urlsafe_b64decode(padded_info)
        return json.loads(decoded_info)

    # Fallback keeps direct App Engine testing possible before Gateway is created.
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise ValueError("Missing bearer token")

    return id_token.verify_oauth2_token(
        auth_header.removeprefix("Bearer "),
        requests.Request(),
        "Replace Client ID"
    )

def _set_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = request.origin or "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Max-Age"] = "3600"
    return resp

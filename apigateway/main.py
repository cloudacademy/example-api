from flask import Flask, request, make_response
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["OPTIONS"])
def preflight():
    # Return a 200 response with CORS headers set for preflight OPTIONS requests
    return _set_cors_headers(make_response())

@app.route("/", methods=["GET"])
def hello():
    # Verify the token from access_token url parameter
    id_info = id_token.verify_oauth2_token(
        request.args.get("access_token"),
        requests.Request(),
        "Replace Client ID"
    )

    # Return a message including the name claim of the token
    resp = make_response(f"Welcome {id_info['name']}")
    return _set_cors_headers(resp)

def _set_cors_headers(resp):
    resp.access_control_allow_credentials = True
    resp.headers["Access-Control-Allow-Origin"] = request.origin
    resp.headers["Access-Control-Allow-Methods"] = "GET"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Max-Age"] = "3600"
    return resp

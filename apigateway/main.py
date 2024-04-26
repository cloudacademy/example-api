from flask import Flask, request, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET","OPTIONS"])
def hello():

    resp = make_response("Welcome CA")
    resp.access_control_allow_credentials = True
    resp.headers["Access-Control-Allow-Origin"] = request.origin
    resp.headers["Access-Control-Allow-Methods"] = "GET"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Max-Age"] = "3600"
    return resp
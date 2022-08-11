from flask import Flask, jsonify, session, request, abort
from flask_cors import CORS
from secrets import token_urlsafe

app = Flask(__name__)
app.secret_key = token_urlsafe(32)
CORS(app, resources={r"/*": {"origins": "*"}})
app.url_map.strict_slashes = False


@app.errorhandler(404)
def resource_not_found(err):
    return jsonify(error=str(err)), 404


@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return "pong", 200

# Import routes and handlers to make the app useful
from . import auth, chat
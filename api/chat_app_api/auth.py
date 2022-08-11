from flask import session, abort

from .app import app
from .models import DoesNotExist, UniqueViolation, User

@app.route('/user/<name>/signin', methods=['POST'])
def signin(name):
    try:
        user = User.objects.get(username=name)
    except DoesNotExist:
        abort(404)

    session['username'] = user.username
    return "you're in, baby!", 200

@app.route('/bye', methods=['POST'])
def bye():
    del session['username']
    return "see yah, Felicia", 200


@app.route('/user/<name>/create', methods=['POST'])
def create_user(name):
    with app.db.cursor() as c:
        try:
            user = User.create(username=name)
            return f"welcome, {name}", 200
        except UniqueViolation:
            return f"sorry, {name} already registered", 422
        except Exception as e:
            return f"oops- that didn't work", 500

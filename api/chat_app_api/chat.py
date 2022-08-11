from datetime import datetime
from flask import session, abort, request, jsonify

from .models import ChatMessage, User, ChatRoom
from .models import DoesNotExist, UniqueViolation

from .app import app

@app.route('/room/<name>/create', methods=['POST'])
def create_room(name):
    if 'username' not in session:
        return "Login required first", 422

    try:
        user = User.objects.get(username=session['username'])
    except DoesNotExist:
        return "Login required first", 422

    try:
        ChatRoom.create(name=name, creator=user.id)
        return f"successfully created a room, {name}", 200
    except UniqueViolation:
        return f"sorry, {name} already exists", 422
    except Exception as e:
        return f"oops- that didn't work: " + repr(e), 500

@app.route('/room/list', methods=['GET'])
def list_rooms():
    if 'username' not in session:
        return "Login required first", 422

@app.route('/room/<name>/subscribe', methods=['POST'])
def join_room(name):
    if 'username' not in session:
        return "Login required first", 422

    try:
        ChatRoom.objects.get(name=name)
    except DoesNotExist:
        return "this room doesn't seem to exist (yet?)", 422

    rooms = session.setdefault('rooms', list())
    if name not in rooms:
        rooms.append(name)

    return f"the followers of {name} welcome you", 200

@app.route('/room/<name>/leave', methods=['POST'])
def leave_room(name):
    if 'username' not in session:
        return "Login required first", 422

    if 'rooms' not in session:
        return "you never joined this room", 422

    rooms = session['rooms']
    rooms.remove(name)

    return f"the followers of {name} bid you adieu", 200

@app.route('/room/<name>/publish', methods=['POST'])
def publish_message(name):
    if 'username' not in session:
        return "Login required first", 422

    try:
        user = User.objects.get(username=session['username'])
    except DoesNotExist:
        return "Login required first", 422

    if 'rooms' not in session \
            or name not in session['rooms']:
        "you never joined this room", 422

    try:
        room = ChatRoom.objects.get(name=name)
    except DoesNotExist:
        return "this room doesn't seem to exist (yet?)", 422

    try:
        content = request.form.get('content')
        msg = ChatMessage.create(poster=user.id, room=room.id,
            posted_at=datetime.now(), content=content)
        return f"you message id is {msg.id} {content!r}", 200
    except Exception as e:
        return "oops, that didn't work: " + repr(e), 500

@app.route('/room/<name>/activity', methods=['GET'])
def get_recent_messages(name):
    if 'username' not in session:
        return "Login required first", 422

    try:
        user = User.objects.get(username=session['username'])
    except DoesNotExist:
        return "Login required first", 422

    if 'rooms' not in session \
            or name not in session['rooms']:
        return "you never joined this room", 422

    # Compiles to:
    # SELECT T0.posted_at, T1.username, T0.content
    #     FROM chat.message T0
    #     JOIN chat.room T2 ON (T0.room = T2.id)
    #     JOIN chat.user T1 ON (T0.poster = T1.id)
    #     WHERE T2.name = %s
    #     ORDER BY posted_at DESC LIMIT 50 OFFSET 0
    recents = ChatMessage.objects \
        .filter(room__name=name) \
        .values(
            'posted_at',
            'poster__username',
            'content',
        ) \
        .ordering('-posted_at')[:50]

    return jsonify(list(recents)), 200
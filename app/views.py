import json

from app import app, USERS, models
from flask import request, Response
from http import HTTPStatus


@app.route("/")
def index():
    return "Hello world!"


@app.post("/user/create")
def user_create():
    data = request.get_json()
    id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    # todo: check email for validity

    user = models.User(id, first_name, last_name, email, posts=[])
    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.OK,
        mimetype="application.json",
    )
    return response

import json

from app import app, USERS, models
from flask import request, Response
from http import HTTPStatus


@app.post("/user/create")  # creation of user
def user_create():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    if not models.User.is_valid_email(email):  # email format validity
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.User(user_id, first_name, last_name, email, posts=[])
    USERS.append(user)
    response = Response(
        json.dumps(user.to_dict()),  # return object type User as a dictionary
        HTTPStatus.OK,
        mimetype="application.json",
    )
    return response


@app.get("/user/<int:user_id>")  # get_user
def get_user(user_id):
    if not models.User.is_existing_user(user_id):  # user existence validity
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = USERS[user_id]
    response = Response(
        json.dumps(user.to_dict()),  # return object type User as a dictionary
        HTTPStatus.OK,
        mimetype="application.json",
    )
    return response

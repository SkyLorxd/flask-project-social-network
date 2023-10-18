import json

from app import app, USERS, models, POSTS
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
    if not models.User.is_valid_email(email):  # email format validity
        return Response(status=HTTPStatus.BAD_REQUEST)
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


@app.get("/user/<int:user_id>")
def get_user(user_id):
    if not models.User.is_existing_user(user_id):  # user existence validity
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = USERS[user_id]
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


@app.post("/posts/create")
def create_post():
    data = request.get_json()
    id = len(POSTS)
    author_id = data["author_id"]
    text = data["text"]
    if not models.User.is_existing_user(author_id):  # user existence validity
        return Response(status=HTTPStatus.BAD_REQUEST)
    post = models.Post(id, author_id, text=text, reactions=[])
    POSTS.append(post)
    for user in range(len(USERS)):
        if USERS[user].id == int(author_id):
            USERS[int(author_id)].posts.append(
                {
                    "id": post.id,
                    "text": post.text,
                    "reactions": post.reactions,
                }
            )
    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application.json",
    )
    return response


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    if not models.Post.is_existing_post(post_id):  # post existence validity
        return Response(status=HTTPStatus.BAD_REQUEST)
    post = POSTS[post_id]
    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application.json",
    )
    return response


@app.post("/posts/<int:post_id>/reaction")
def add_reaction(post_id):  # todo: make avalible to add only one reaction per user
    data = request.get_json()
    user_id = data["user_id"]
    reaction = data[
        "reaction"
    ]  # expect : "like", "funny", "heart", "cool", "fire", "angry", "cry"
    if not models.Post.is_existing_post(post_id):  # post existence validity
        return Response(status=HTTPStatus.BAD_REQUEST)
    if not models.User.is_existing_user(user_id):  # user existence validity
        return Response(status=HTTPStatus.BAD_REQUEST)
    if not reaction in {
        "like",
        "funny",
        "heart",
        "cool",
        "fire",
        "angry",
        "cry",
    }:  # reaction existence validity
        return Response(status=HTTPStatus.BAD_REQUEST)
    for user in range(len(USERS)):
        if USERS[user].id == int(user_id):
            USERS[user].total_reactions += 1
    for post in range(len(POSTS)):
        if POSTS[post].id == int(post_id):
            POSTS[post].reactions.append(reaction)
    response = Response(status=HTTPStatus.OK)
    return response

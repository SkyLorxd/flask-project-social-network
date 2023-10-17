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

    if not models.User.is_valid_email(email):
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
    if user_id > len(USERS) - 1 or user_id < 0:
        return Response(status=HTTPStatus.NOT_FOUND)
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

    if not models.Post.is_existing_user(author_id):
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
    if post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.NOT_FOUND)
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

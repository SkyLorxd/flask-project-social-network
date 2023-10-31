import json

from app import app, USERS, models, POSTS
from flask import request, Response
from http import HTTPStatus


@app.post("/posts/create")  # creation of post
def create_post():
    data = request.get_json()
    post_id = len(POSTS)
    author_id = data["author_id"]
    text = data["text"]

    if not models.User.is_existing_user(author_id):  # user existence validity
        return Response(status=HTTPStatus.BAD_REQUEST)

    post = models.Post(post_id, author_id, text=text, reactions=[])
    POSTS.append(post)

    for user in range(len(USERS)):  # adds post info to object type User
        if USERS[user].id == int(author_id):
            USERS[int(author_id)].posts.append(
                post.to_dict()
            )  # appends Post as a dictionary

    response = Response(
        json.dumps(post.to_dict()),  # return object type Post as a dictionary
        HTTPStatus.OK,
        mimetype="application.json",
    )
    return response


@app.get("/posts/<int:post_id>")  # view of post
def get_post(post_id):
    if not models.Post.is_existing_post(post_id):  # post existence validity
        return Response(status=HTTPStatus.BAD_REQUEST)

    post = POSTS[post_id]
    response = Response(
        json.dumps(post.to_dict()),  # return object type Post as a dictionary
        HTTPStatus.OK,
        mimetype="application.json",
    )
    return response


@app.get("/users/<int:user_id>/posts")
def get_user_posts(user_id):
    if not models.User.is_existing_user(user_id):  # user existence validity
        return Response(status=HTTPStatus.BAD_REQUEST)

    data = request.get_json()
    sort = data["sort"]

    if not (sort == "asc" or sort == "desc"):  # sort type validity
        return Response(status=HTTPStatus.BAD_REQUEST)

    user_posts = None

    while not user_posts:  # creates unsorted list of posts
        for user in range(len(USERS)):
            if USERS[user].id == int(user_id):
                user_posts = USERS[user].posts
        break

    for _ in range(  # sorts the user posts list by quantity of reactions
        len(user_posts) - 1
    ):
        for __ in range(len(user_posts) - 1):
            if len(user_posts[__]["reactions"]) > len(user_posts[__ + 1]["reactions"]):
                user_posts[__], user_posts[__ + 1] = (
                    user_posts[__ + 1],
                    user_posts[__],
                )

    if sort == "asc":
        response = Response(
            json.dumps(
                {
                    "posts": user_posts,
                }
            ),
            HTTPStatus.OK,
            mimetype="application.json",
        )
        return response

    if sort == "desc":
        response = Response(
            json.dumps({"posts": [user_posts[::-1]]}),  # reversed list of user posts
            HTTPStatus.OK,
            mimetype="application.json",
        )
        return response

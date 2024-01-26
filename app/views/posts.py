import json

from app import app, USERS, models, POSTS
from flask import request, Response
from http import HTTPStatus


@app.post("/posts/create")  # creation of post
def create_post():
    data = request.get_json()
    post_id = 100000000 + len(POSTS)
    author_id = data["author_id"]
    text = data["text"]

    if not models.User.is_existing_user(author_id):  # user existence validity
        return Response(
            f"User with id: {author_id} does not exist", status=HTTPStatus.BAD_REQUEST
        )

    if not models.User.is_active(author_id):  # user status validity
        return Response(
            f"User with id: {author_id} was deleted", status=HTTPStatus.BAD_REQUEST
        )

    post = models.Post(post_id, author_id, text=text, status="active", reactions=[])
    POSTS.append(post)

    for user in range(len(USERS)):  # adds post info to object type User
        if USERS[user].id == int(author_id):
            author = USERS[user]
            author.posts.append(post.to_dict())  # appends Post as a dictionary

    response = Response(
        json.dumps(post.to_dict()),  # return object type Post as a dictionary
        HTTPStatus.OK,
        mimetype="application.json",
    )
    return response


@app.get("/posts/<int:post_id>")  # view of post
def get_post(post_id):
    response = Response(
        f"Post with id: {post_id} does not exist", status=HTTPStatus.BAD_REQUEST
    )

    for post in range(len(POSTS)):
        if POSTS[post].id == post_id:
            post = POSTS[post]
            response = Response(
                json.dumps(post.to_dict()),  # return object type Post as a dictionary
                HTTPStatus.OK,
                mimetype="application.json",
            )
    return response


@app.get("/users/<int:user_id>/posts")
def get_user_posts(user_id):
    if not models.User.is_existing_user(user_id):  # user existence validity
        return Response(
            f"User with id: {user_id} does not exist.", status=HTTPStatus.BAD_REQUEST
        )

    if not models.User.is_active(user_id):  # user status validity
        return Response(
            f"User with id: {user_id} was deleted", status=HTTPStatus.BAD_REQUEST
        )

    data = request.get_json()
    sort = data["sort"]

    if not (sort == "asc" or sort == "desc"):  # sort type validity
        return Response("Wrong sort type.", status=HTTPStatus.BAD_REQUEST)

    user_posts = None

    while not user_posts:  # creates unsorted list of posts
        for user in range(len(USERS)):
            if USERS[user].id == int(user_id):
                # user_posts = USERS[user].posts
                user_posts = list(
                    filter(lambda post: post["status"] == "active", USERS[user].posts)
                )
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


@app.delete("/posts/delete/<int:post_id>")
def delete_post(post_id):
    if not models.Post.is_existing_post(post_id):
        return Response(
            f"Post with id: {post_id} does not exist", status=HTTPStatus.BAD_REQUEST
        )
    for post in POSTS:
        if post.id == post_id:
            post.status = "deleted"
            user_id = int(post.author_id)
            for user in USERS:
                if user.id == user_id:
                    for user_post in user.posts:
                        if user_post["id"] == post_id:
                            user_post["status"] = "deleted"
    return Response(f"Post with id: {post_id} was deleted", status=HTTPStatus.OK)

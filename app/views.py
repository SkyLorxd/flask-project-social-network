import json

from app import app, USERS, models, POSTS
from flask import request, Response
from http import HTTPStatus


@app.route("/")  # home page
def index():
    return "Hello world!"


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


@app.post("/posts/<int:post_id>/reaction")  # addition of reaction to post
def add_reaction(post_id):
    if not models.Post.is_existing_post(post_id):  # post existence validity
        return Response(status=HTTPStatus.BAD_REQUEST)

    data = request.get_json()
    user_id = data["user_id"]

    if not models.User.is_existing_user(user_id):  # user existence validity
        return Response(status=HTTPStatus.BAD_REQUEST)
    for post in range(len(POSTS)):  # check if user has already reacted to this post
        if POSTS[post].id == int(post_id):
            for reaction in range(len(POSTS[post].reactions)):
                if POSTS[post].reactions[reaction].get("user_id") == user_id:
                    return Response(status=HTTPStatus.BAD_REQUEST)

    reaction_type = data[
        "reaction"
    ]  # expect : "like", "funny", "heart", "cool", "fire", "angry", "cry"
    if not models.Reaction.is_existing_reaction(  # reaction type validity
        reaction_type
    ):
        return Response(status=HTTPStatus.BAD_REQUEST)

    reaction = models.Reaction(post_id, user_id, reaction_type)

    for post in range(len(POSTS)):  # adds reaction to reaction counter of posts author
        if POSTS[post].id == int(post_id):
            author_id = POSTS[post].author_id
            for user in range(len(USERS)):
                if USERS[user].id == int(author_id):
                    USERS[user].total_reactions += 1

    for post in range(  # adds reaction to reactions list of object type Post
        len(POSTS)
    ):
        if POSTS[post].id == int(post_id):
            POSTS[post].reactions.append(reaction.to_dict())

    response = Response(status=HTTPStatus.OK)

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

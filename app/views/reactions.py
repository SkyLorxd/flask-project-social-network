from app import app, USERS, models, POSTS
from flask import request, Response
from http import HTTPStatus


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

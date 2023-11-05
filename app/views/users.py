import json

from app import app, USERS, models
from flask import request, Response, url_for
from http import HTTPStatus
import matplotlib.pyplot as plt


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


@app.get("/users/leaderboard")  # leaderboard of users by total reactions
def get_users_leaderboard():
    data = request.get_json()
    leaderboard_type = data["type"]
    sort = data["sort"]

    if sort not in ["asc", "desc"]:  # sort type validity
        return Response(status=HTTPStatus.BAD_REQUEST)

    USERS.sort()
    user_names = models.User.get_leaderboard()

    if leaderboard_type == "list":
        if sort == "asc":
            return user_names
        if sort == "desc":
            return user_names[::-1]

    elif leaderboard_type == "graph":
        fig, ax = plt.subplots()
        user_total_reactions = [user.total_reactions for user in USERS]
        if sort == "asc":
            ax.bar(user_names, user_total_reactions)
        if sort == "desc":
            ax.bar(user_names, user_total_reactions[::-1])

        ax.set_ylabel("Total reactions")
        ax.set_title("Total reactions on users posts")
        plt.savefig("app/static/user_leaderboard.png")
        return Response(
            f"""<img src="{url_for('static',filename = 'user_leaderboard.png')}">""",
            status=HTTPStatus.OK,
            mimetype="text/html",
        )
    else:  # leaderboard_type validity
        return Response(status=HTTPStatus.BAD_REQUEST)

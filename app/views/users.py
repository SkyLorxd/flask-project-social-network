import json

from app import app, USERS, models
from flask import request, Response, url_for
from http import HTTPStatus
import matplotlib.pyplot as plt


@app.post("/user/create")  # creation of user
def user_create():
    data = request.get_json()
    user_id = 100000000 + len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    status = data["status"]

    if not models.User.is_valid_email(email):  # email format validity
        return Response(
            "Wrong email! Check email format.", status=HTTPStatus.BAD_REQUEST
        )

    user = models.User(user_id, first_name, last_name, email, status, posts=[])
    USERS.append(user)
    response = Response(
        json.dumps(user.to_dict()),  # return object type User as a dictionary
        HTTPStatus.OK,
        mimetype="application.json",
    )
    return response


@app.get("/user/<int:user_id>")  # get_user
def get_user(user_id):
    response = Response(
        f"User with id: {user_id} does not exist", status=HTTPStatus.BAD_REQUEST
    )

    for user in range(len(USERS)):
        if USERS[user].id == user_id:
            user = USERS[user]
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
        return Response("Incorrect sort type.", status=HTTPStatus.BAD_REQUEST)

    USERS.sort()
    users_info = models.User.get_leaderboard()
    user_names = [user["name"] for user in users_info]
    user_total_reactions = [int(user["total_reactions"]) for user in users_info]

    if leaderboard_type == "list":
        if sort == "asc":
            return users_info
        if sort == "desc":
            return users_info[::-1]

    elif leaderboard_type == "graph":
        fig, ax = plt.subplots()
        if sort == "asc":
            ax.bar(user_names, user_total_reactions)
        if sort == "desc":
            ax.bar(user_names[::-1], user_total_reactions[::-1])

        ax.set_ylabel("Total reactions")
        ax.set_title("Total reactions on users posts")
        user_total_reactions.append(0)
        user_total_reactions.sort()
        plt.yticks(user_total_reactions)
        plt.savefig("app/static/user_leaderboard.png")

        return Response(
            f"""<img src="{url_for('static',filename = 'user_leaderboard.png')}">""",
            status=HTTPStatus.OK,
            mimetype="text/html",
        )
    else:  # leaderboard_type validity
        return Response(
            "Leaderboard type must be list or graph.", status=HTTPStatus.BAD_REQUEST
        )


@app.delete("/user/delete/<int:user_id>")
def delete_user(user_id):
    if not models.User.is_existing_user(user_id):
        return Response(f"User with id: {user_id} does not exist", status=HTTPStatus.BAD_REQUEST)
    for user in range(len(USERS)):
        if USERS[user].id == user_id:
            USERS[user].status = "deleted"
    return Response(f"User with id: {user_id} was deleted", status=HTTPStatus.OK)
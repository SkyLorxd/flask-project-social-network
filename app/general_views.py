from app import app, USERS, POSTS, REACTIONS


@app.route("/")  # home page
def index():
    response = (
        f"<h1>Welcome to home page!</h1>"
        f"USERS:<br>{'<br>'.join([user.repr() for user in USERS])}<br>"
        "<br>"
        f"POSTS:<br>{'<br>'.join([post.repr() for post in POSTS])}<br>"
        "<br>"
        f"REACTIONS:<br>{'<br>'.join(*[REACTIONS])}<br>"
    )
    return response

from flask import Flask

app = Flask(__name__)

USERS = []  # List for objects type: User
POSTS = []  # List for objects type: Post
REACTIONS = [
    "like",
    "funny",
    "heart",
    "cool",
    "fire",
    "angry",
    "cry",
]  # List of possible reaction types

from app import views
from app import models

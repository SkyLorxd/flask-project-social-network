from flask import Flask

app = Flask(__name__)

USERS = []  # List for objects type: User
POSTS = []  # List for objects type: Post
REACTIONS = []

from app import views
from app import models

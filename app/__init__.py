from flask import Flask

app = Flask(__name__)

USERS = []  # List for objects type: User
POSTS = []  # List for objects type: Post

from app import views
from app import models

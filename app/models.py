# models.py
import re

from app import USERS, POSTS, REACTIONS


class User:
    def __init__(self, user_id, first_name, last_name, email, posts, total_reactions=0):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = posts

    def __lt__(self, other):
        return self.total_reactions < other.total_reactions

    def repr(self):
        return f"{self.id}) {self.last_name} {self.first_name}"

    def to_dict(self):  # return object type User as a dictionary
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "total_reactions": self.total_reactions,
            "posts": self.posts,
        }

    @staticmethod
    def is_valid_email(email):  # email validity check
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    @staticmethod
    def is_existing_user(user_id):  # user existence check
        for user in range(len(USERS)):
            if USERS[user].id == int(user_id):
                return True
        return False

    @staticmethod
    def get_leaderboard():
        return [
            user.last_name + " " + user.first_name + " id:" + str(user.id) for user in USERS
        ]


class Post:
    def __init__(self, post_id, author_id, reactions, text=""):
        self.id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = reactions

    def to_dict(self):  # return object type Post as a dictionary
        return {
            "id": self.id,
            "author_id": self.author_id,
            "text": self.text,
            "reactions": self.reactions,
        }

    def repr(self):
        return f"{self.id}) text: {self.text}; reactions: {len(self.reactions)}"

    @staticmethod
    def is_existing_post(post_id):  # post existence check
        for post in range(len(POSTS)):
            if POSTS[post].id == int(post_id):
                return True
        return False


class Reaction:
    def __init__(self, post_id, user_id, reaction_type):
        self.post_id = post_id
        self.user_id = user_id
        self.reaction_type = reaction_type

    def to_dict(self):  # represents reaction in dictionary format
        return {
            "post_id": self.post_id,
            "user_id": self.user_id,
            "reaction_type": self.reaction_type,
        }

    @staticmethod
    def is_existing_reaction(reaction_type):  # reaction_type existence check
        if reaction_type in set(REACTIONS):
            return True
        return False

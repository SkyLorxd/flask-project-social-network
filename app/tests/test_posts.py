from http import HTTPStatus

# import pytest
import requests


def create_user_payload():
    return {
        "first_name": "Kolya",
        "last_name": "Zubkin",
        "email": "test@test.com",
        "status": "active",
    }


def test_posts():
    user_payload = create_user_payload()

    user_response = requests.post(
        "http://127.0.0.1:5000/user/create", json=user_payload
    )

    user_data = user_response.json()

    post_payload = {
        "author_id": f"{user_data['id']}",
        "text": "izi otladil kod0",
    }

    post_response = requests.post(
        "http://127.0.0.1:5000/posts/create", json=post_payload
    )

    post_data = post_response.json()

    assert post_response.status_code == HTTPStatus.OK

    get_user_response = requests.get(f"http://127.0.0.1:5000/user/{user_data['id']}")

    assert isinstance(get_user_response.json()["posts"], list)
    assert len(get_user_response.json()["posts"]) == 1
    assert post_data["author_id"] == post_payload["author_id"]
    assert post_data["text"] == post_payload["text"]
    assert post_data["status"] == "active"

    get_posts_response = requests.get(f"http://127.0.0.1:5000/posts/{post_data['id']}")

    assert get_posts_response.status_code == HTTPStatus.OK
    assert get_posts_response.json()["id"] == post_data["id"]
    assert get_posts_response.json()["author_id"] == post_data["author_id"]
    assert get_posts_response.json()["text"] == post_data["text"]
    assert get_posts_response.json()["reactions"] == post_data["reactions"]
    assert get_posts_response.json()["status"] == post_data["status"]

    get_user_posts_response = requests.get(
        f"http://127.0.0.1:5000/users/{user_data['id']}/posts", json={"sort": "asc"}
    )

    assert get_user_posts_response.status_code == HTTPStatus.OK
    assert isinstance(get_user_posts_response.json()["posts"], list)
    assert len(get_user_posts_response.json()["posts"]) == 1

    requests.delete(f"http://127.0.0.1:5000/user/delete/{user_data['id']}")
    requests.delete(f"http://127.0.0.1:5000/posts/delete/{post_data['id']}")

    get_deleted_post_response = requests.get(
        f"http://127.0.0.1:5000/posts/{post_data['id']}"
    )

    assert get_deleted_post_response.status_code == HTTPStatus.OK
    assert get_deleted_post_response.json()["status"] == "deleted"


def test_post_wrong_data():
    user_payload = create_user_payload()

    create_user_response = requests.post(
        "http://127.0.0.1:5000/user/create", json=user_payload
    )

    user_data = create_user_response.json()

    wrong_author_id_post_payload = {
        "author_id": f"{user_data['id']+1}",
        "text": "izi otladil kod0",
    }

    post_response = requests.post(
        "http://127.0.0.1:5000/posts/create", json=wrong_author_id_post_payload
    )

    assert post_response.status_code == HTTPStatus.BAD_REQUEST

    requests.delete(f"http://127.0.0.1:5000/user/delete/{user_data['id']}")

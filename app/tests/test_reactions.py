from http import HTTPStatus

import requests


def create_user_payload():
    return {
        "first_name": "Kolya",
        "last_name": "Zubkin",
        "email": "test@test.com",
        "status": "active",
    }


def test_reactions():
    user_payload = create_user_payload()
    user_response = requests.post(
        "http://127.0.0.1:5000/user/create", json=user_payload
    )
    user_id = user_response.json()["id"]
    assert user_response.status_code == HTTPStatus.OK

    post_payload = {
        "author_id": f"{user_id}",
        "text": "izi otladil kod0",
    }
    post_response = requests.post(
        "http://127.0.0.1:5000/posts/create", json=post_payload
    )
    post_id = post_response.json()["id"]
    assert post_response.status_code == HTTPStatus.OK

    reaction_payload = {"user_id": f"{user_id}", "reaction": "cool"}
    reaction_response = requests.post(
        f"http://127.0.0.1:5000/posts/{post_id}/reaction", json=reaction_payload
    )
    assert reaction_response.status_code == HTTPStatus.OK

    post_get_response = requests.get(f"http://127.0.0.1:5000/posts/{post_id}")

    assert isinstance(post_get_response.json()["reactions"], list)
    assert len(post_get_response.json()["reactions"]) == 1
    assert (
        post_get_response.json()["reactions"][0]["reaction_type"]
        == reaction_payload["reaction"]
    )

    requests.delete(f"http://127.0.0.1:5000/user/delete/{user_id}")
    requests.delete(f"http://127.0.0.1:5000/posts/delete/{post_id}")


def test_reactions_wrong_data():
    user_payload = create_user_payload()
    user_response = requests.post(
        "http://127.0.0.1:5000/user/create", json=user_payload
    )
    user_id = user_response.json()["id"]
    assert user_response.status_code == HTTPStatus.OK

    post_payload = {
        "author_id": f"{user_id}",
        "text": "izi otladil kod0",
    }
    post_response = requests.post(
        "http://127.0.0.1:5000/posts/create", json=post_payload
    )
    post_id = post_response.json()["id"]
    assert post_response.status_code == HTTPStatus.OK

    reaction_payload = {"user_id": f"{user_id}", "reaction": "cool"}
    reaction_response_wrong_post_id = requests.post(
        f"http://127.0.0.1:5000/posts/{post_id+1}/reaction", json=reaction_payload
    )
    assert reaction_response_wrong_post_id.status_code == HTTPStatus.BAD_REQUEST

    reaction_payload_wrong_user_id = {
        "user_id": f"{user_id+1}",
        "reaction": "cool",
    }
    reaction_response_wrong_user_id = requests.post(
        f"http://127.0.0.1:5000/posts/{post_id}/reaction",
        json=reaction_payload_wrong_user_id,
    )
    assert reaction_response_wrong_user_id.status_code == HTTPStatus.BAD_REQUEST

    reaction_payload_wrong_reaction_type = {
        "user_id": f"{user_id}",
        "reaction": "col",
    }
    reaction_response_wrong_user_id = requests.post(
        f"http://127.0.0.1:5000/posts/{post_id}/reaction",
        json=reaction_payload_wrong_reaction_type,
    )
    assert reaction_response_wrong_user_id.status_code == HTTPStatus.BAD_REQUEST

    requests.delete(f"http://127.0.0.1:5000/user/delete/{user_id}")
    requests.delete(f"http://127.0.0.1:5000/posts/delete/{post_id}")

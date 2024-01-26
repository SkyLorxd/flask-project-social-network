from http import HTTPStatus

import requests


def create_user_payload():
    return {
        "first_name": "Vasya",
        "last_name": "Supkin",
        "email": "test@test.com",
        "status": "active",
    }


def test_users():
    payload = create_user_payload()
    create_response = requests.post(f"http://127.0.0.1:5000/user/create", json=payload)

    assert (
        create_response.status_code == HTTPStatus.OK
    )  # status code of creation request validity

    user_data = create_response.json()
    assert isinstance(user_data["id"], int)  # validity of id data type
    assert user_data["total_reactions"] == 0  # validity of correct reactions count
    assert user_data["posts"] == []  # checks if posts is an empty list
    assert user_data["status"] == "active"  # user status check

    delete_request = requests.delete(
        f"http://127.0.0.1:5000/user/delete/{user_data['id']}"
    )
    assert delete_request.status_code == HTTPStatus.OK
    # assert delete_request.json()["status"] == "deleted"

    get_response = requests.get(f"http://127.0.0.1:5000/user/{user_data['id']}")
    assert get_response.status_code == HTTPStatus.OK  # checks response code
    assert (
        get_response.json()["status"] == "deleted"
    )  # checks if user status was changed to "deleted"


def test_users_wrong_data():
    payload_wrong_email = {
        "first_name": "Vasya",
        "last_name": "Supkin",
        "email": "testtest.com",
        "status": "active",
    }
    response_wrong_email = requests.post(
        "http://127.0.0.1:5000/user/create", json=payload_wrong_email
    )
    assert (
        response_wrong_email.status_code == HTTPStatus.BAD_REQUEST
    )  # checks if response code with wrong email is 400

    wrong_user_id = 0
    response_wrong_user_id = requests.get(f"http://127.0.0.1:5000/user/{wrong_user_id}")
    assert (
        response_wrong_user_id.status_code == HTTPStatus.BAD_REQUEST
    )  # checks if response code with wrong user id is 400


def test_leaderboard():
    payload_user_1 = create_user_payload()
    payload_user_2 = create_user_payload()
    user_response_1 = requests.post(
        "http://127.0.0.1:5000/user/create", json=payload_user_1
    )
    user_response_2 = requests.post(
        "http://127.0.0.1:5000/user/create", json=payload_user_2
    )

    list_leaderboard_payload_asc = {"type": "list", "sort": "asc"}
    list_leaderboard_payload_desc = {"type": "list", "sort": "desc"}
    list_leaderboard_response_asc = requests.get(
        "http://127.0.0.1:5000/users/leaderboard", json=list_leaderboard_payload_asc
    )
    list_leaderboard_response_desc = requests.get(
        "http://127.0.0.1:5000/users/leaderboard", json=list_leaderboard_payload_desc
    )

    assert (
        list_leaderboard_response_asc.status_code == HTTPStatus.OK
    )  # checks if response code is 200
    assert (
        list_leaderboard_response_desc.status_code == HTTPStatus.OK
    )  # checks if response code is 200

    assert isinstance(
        list_leaderboard_response_asc.json(), list
    )  # checks if request returns list
    assert len(list_leaderboard_response_asc.json()) == 2  # checks if list length == 2
    assert (
        list_leaderboard_response_asc.json()[0]["total_reactions"]
        <= list_leaderboard_response_asc.json()[1]["total_reactions"]
    )  # checks if leaderboard sort is correct
    assert (
        list_leaderboard_response_desc.json()[0]["total_reactions"]
        >= list_leaderboard_response_desc.json()[1]["total_reactions"]
    )  # checks if leaderboard sort is correct

    requests.delete(f"http://127.0.0.1:5000/user/delete/{user_response_1.json()['id']}")
    requests.delete(f"http://127.0.0.1:5000/user/delete/{user_response_2.json()['id']}")

import pytest
import requests


def test_create_application():
    with requests.Session() as ac:
        response = ac.post(
            "http://127.0.0.1:8000/applications/", json={"user_name": "test_user", "description": "test_description"}
        )
        assert response.status_code == 200
        assert response.json()["user_name"] == "test_user"


def test_list_applications():
    with requests.Session() as ac:
        response = ac.get(
            "http://127.0.0.1:8000/applications/", params={"user_name": "test_user", "page": 1, "size": 10}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_list_applications_without_user_name():
    with requests.Session() as ac:
        response = ac.get("http://127.0.0.1:8000/applications/", params={"page": 1, "size": 10})
        assert response.status_code == 200
        assert isinstance(response.json(), list)

import pytest
from helpers import *
from data import APILinks
import requests


@pytest.fixture(scope="function")
def create_and_delete_user():
    payload = create_user_data()
    login_data = payload.copy()
    response = requests.post(APILinks.MAIN_URL+APILinks.REGISTER_URL, data=payload)
    token = response.json()["accessToken"]
    yield payload, login_data, token
    requests.delete(APILinks.MAIN_URL + APILinks.USER_URL, headers={'Authorization': f'{token}'})

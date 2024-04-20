import pytest
import allure
import requests
from data import APILinks, UserData, Error
from helpers import create_user_data


class TestCreateUser:
    @allure.title('Successful new user registration')
    def test_create_new_user_success(self):
        payload = create_user_data()
        r = requests.post(APILinks.MAIN_URL + APILinks.REGISTER_URL, data=payload)
        assert r.status_code == 200 and r.json().get("success") is True

    @allure.title('Error when creating a user with data from an already registered user')
    def test_create_user_with_duplicate_data_fail(self, create_and_delete_user):
        r = requests.post(APILinks.MAIN_URL + APILinks.REGISTER_URL, data=create_and_delete_user[0])
        assert r.status_code == 403 and r.json()['message'] == Error.ALREADY_EXISTS

    @allure.title('Error when creating a user without required fields')
    @pytest.mark.parametrize('payload', (UserData.without_name, UserData.without_email, UserData.without_password))
    def test_create_user_without_required_fields_fail(self, payload):
        r = requests.post(APILinks.MAIN_URL + APILinks.REGISTER_URL, data=payload)
        assert r.status_code == 403 and r.json()['message'] == Error.EMPTY_FIELDS

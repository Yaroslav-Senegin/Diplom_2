import allure
import requests
from data import APILinks, IngredientsData


class TestCreateOrder:
    @allure.title('Successful creation of an order by an authorized user')
    def test_create_order_authorised_user_success(self, create_and_delete_user):
        token = {'Authorization': create_and_delete_user[3]}
        r = requests.post(APILinks.MAIN_URL + APILinks.ORDERS_URL, headers=token,
                           data=IngredientsData.correct_ingredients)
        assert r.status_code == 200 and r.json().get("success") is True

    @allure.title('Successful order creation by an unauthorized user')
    def test_create_order_user_without_authorisation_success(self):
        r = requests.post(APILinks.MAIN_URL + APILinks.ORDERS_URL,
                           data=IngredientsData.correct_ingredients)
        assert r.status_code == 200 and r.json().get("success") is True

    @allure.title('Successfully creating an order without ingredients')
    def test_create_order_without_ingredients_fail(self):
        r = requests.post(APILinks.MAIN_URL + APILinks.ORDERS_URL)
        assert r.status_code == 400 and r.json()['message'] == "Ingredient ids must be provided"

    @allure.title('Error when creating an order with an incorrect ingredient hash')
    def test_create_order_incorrect_hash_fail(self):
        r = requests.post(APILinks.MAIN_URL + APILinks.ORDERS_URL,
                           data=IngredientsData.incorrect_ingredients)
        assert r.status_code == 500 and 'Internal Server Error' in r.text

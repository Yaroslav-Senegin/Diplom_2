import allure
import requests
from data import APILinks, IngredientsData


class TestGetOrder:
    @allure.title('Successful receipt of an order by an authorized user')
    def test_get_order_with_authorized_user_success(self, create_and_delete_user):
        token = {'Authorization': create_and_delete_user[3]}
        requests_create_order = requests.post(APILinks.MAIN_URL + APILinks.ORDERS_URL,
                                               headers=token, data=IngredientsData.correct_ingredients)
        response_get_order = requests.get(APILinks.MAIN_URL + APILinks.ORDERS_URL, headers=token)
        assert response_get_order.status_code == 200 and \
        response_get_order.json()['orders'][0]['number'] == requests_create_order.json()['order']['number']

    @allure.title('Error when receiving an order by an unauthorized user')
    def test_get_order_user_without_authorization_fail(self):
        r = requests.get(APILinks.MAIN_URL + APILinks.ORDERS_URL)
        assert r.status_code == 401 and r.json()['message'] == "You should be authorised"

import pytest
import allure


@pytest.mark.VK_API
@allure.feature('VK API')
class TestVkApi:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, vk_api_client):
        self.client = vk_api_client

    @allure.title('Получение vk id пользователя')
    def test_get_positive(self):
        """
        Тестируется получение существуюшего vk_id пользователя.
        Для заданного пользователя ожидается результат с кодом 200.
        """
        response = self.client.get_user('ikramanop')

        assert response.status_code == 200
        assert 'vk_id' in response.json().keys()
        assert response.json()['vk_id'] == 315368721

    @allure.title('Получение пустого ответа')
    def test_get_negative(self):
        """
        Тестируется получение пустого ответа.
        Для заданного пользователя не ожидается результат (код 404).
        """
        response = self.client.get_user('fnsjh3fn23i')

        assert response.status_code == 404
        assert len(response.json()) == 0
        assert response.json() == {}

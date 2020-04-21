import pytest

from api.client import ApiClient


class TestAPI:
    @pytest.fixture(scope='function')
    def api_client(self):
        self.user = 'target_test_123@inbox.ru'
        self.password = 'qwerty1234'

        return ApiClient(self.user, self.password)

    @pytest.fixture(scope='function')
    def segment(self, api_client):
        response = api_client.create_segment()
        yield response
        segment_id = response.json()['id']
        api_client.delete_segment(segment_id)

    @pytest.mark.API
    def test_create_segment(self, segment):
        new_segment = segment
        assert new_segment.status_code == 200
        assert new_segment.json()['name'] == 'segment'

    @pytest.mark.API
    def test_delete_segment(self, api_client):
        response = api_client.create_segment()
        segment_id = response.json()['id']
        delete_response = api_client.delete_segment(segment_id)
        segments = api_client.get_segments()
        assert delete_response.status_code == 204
        for item in segments:
            assert item['id'] != segment_id

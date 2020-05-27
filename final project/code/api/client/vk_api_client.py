import requests


class VkApiClient:

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

        self.session = requests.Session()

    def get_user(self, username):
        return self.session.get(f'http://{self.hostname}:{self.port}/vk_id/{username}')

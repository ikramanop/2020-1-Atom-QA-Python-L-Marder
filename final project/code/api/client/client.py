import json
from time import time
from urllib.parse import urljoin

import requests
from requests.cookies import cookiejar_from_dict


class ApiClient:

    def __init__(self, user, password, url):
        self.url = url

        self.user = user
        self.password = password

        self.session = requests.Session()

        self.response = self.login()

    def login(self):
        data = {
            'username': self.user,
            'password': self.password,
            'submit': 'Login',
        }

        response = self.request(method='POST', location='/login', data=data, redirect=False)
        cookie = response.headers['Set-Cookie'].split(';')[0].split('=')[1]
        self.session.cookies = cookiejar_from_dict({
            'session': cookie
        })
        self.request(method='GET', location='/welcome')

        return response

    def logout(self):
        response = self.request(method='GET', location='/logout', redirect=False)
        new_url = response.headers['Location']
        self.request(method='GET', url=new_url)

    def request(self, method, url=None, location=None, headers=None, params=None, data=None, json=False, redirect=True):
        if url is None:
            url = urljoin(self.url, location)

        response = self.session.request(method, url=url, headers=headers, params=params, data=data,
                                        allow_redirects=redirect)

        if json:
            return response.json()

        return response

    def add_random_user(self):
        username = str(time())[:16]
        data = {
            'username': username,
            'password': '11',
            'email': f'{username}@bb.bb'
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = self.session.request('POST', url='http://127.0.0.1:8082/api/add_user', data=json.dumps(data),
                                        headers=headers)

        return response, username

    def add_random_user_null_password(self):
        username = str(time())[:16]
        data = {
            'username': username,
            'password': None,
            'email': f'{username}@bb.bb'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = self.session.request('POST', url='http://127.0.0.1:8082/api/add_user', data=json.dumps(data),
                                        headers=headers)
        return response, username

    def add_random_user_empty_password(self):
        username = str(time())[:16]
        data = {
            'username': username,
            'password': '',
            'email': f'{username}@bb.bb'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = self.session.request('POST', url='http://127.0.0.1:8082/api/add_user', data=json.dumps(data),
                                        headers=headers)
        return response, username

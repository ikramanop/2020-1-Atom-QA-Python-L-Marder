import json
from urllib.parse import urljoin

import requests
from requests.cookies import cookiejar_from_dict


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, user, password):
        self.base_url = 'https://target.my.com/'
        self.session = requests.Session()

        self.user = user
        self.password = password

        self.login()

        self.csrf = self.get_csrf()

    def request(self, method, url=None, location=None, headers=None, params=None, data=None, json=False, redirect=True):
        if url is None:
            url = urljoin(self.base_url, location)

        response = self.session.request(method, url=url, headers=headers, params=params, data=data,
                                        allow_redirects=redirect)

        if json:
            return response.json()

        return response

    def login(self):
        headers_first = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'auth-ac.my.com',
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/',
        }

        headers_target = {
            'Host': 'target.my.com',
            'Referer': 'https://target.my.com/',
        }

        headers_ac = {
            'Host': 'auth-ac.my.com',
            'Referer': 'https://target.my.com/',
        }

        data = {
            'login': self.user,
            'password': self.password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1#email',
            'failure': 'https://account.my.com/login/',
        }

        log1 = self.request('POST', url='https://auth-ac.my.com/auth?lang=ru&nosavelogin=0', headers=headers_first,
                            data=data, redirect=False)
        url1 = log1.headers['Location']

        cookies = log1.headers['Set-Cookie'].split(';')
        mc = cookies[0].split('=')[-1]
        ssdc = [i for i in cookies if i.startswith(' SameSite=None, ssdc=')][0].split(' ')[2].split('=')[-1]
        mrcu = [i for i in cookies if i.startswith(' SameSite=None, mrcu=')][0].split(' ')[2].split('=')[-1]
        cookies = {'mc': mc, 'ssdc': ssdc, 'mrcu': mrcu}
        self.session.cookies = cookiejar_from_dict(cookies)

        log2 = self.request('GET', url=url1, headers=headers_target, redirect=False)
        url2 = log2.headers['Location']

        log3 = self.request('GET', url=url2, headers=headers_ac, redirect=False)
        url3 = log3.headers['Location']

        log4 = self.request('GET', url=url3, headers=headers_target, redirect=False)
        url4 = log4.headers['Location']

        sdcs = log4.headers['Set-Cookie'].split(';')[0].split('=')[-1]
        cookies['sdcs'] = sdcs
        self.session.cookies = cookiejar_from_dict(cookies)

        headers_final = {
            'Host': 'target.my.com',
            'Referer': 'https://target.my.com/auth/mycom?state=target_login%3D1',
        }

        self.request('GET', url=url4, headers=headers_target)

        return self.request('GET', headers=headers_final, redirect=False)

    def get_csrf(self):
        csrf_headers = {
            'Host': 'target.my.com',
            'Referer': 'https://target.my.com/auth/mycom?state=target_login%3D1',
        }
        log = self.request('GET', location='csrf', headers=csrf_headers)

        return log.headers['Set-Cookie'].split(';')[0].split('=')[-1]

    def create_segment(self):
        location = 'api/v2/remarketing/segments.json'
        headers = {
            'Content-Type': 'application/json',
            'Host': 'target.my.com',
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/segments/segments_list/new',
            'X-CSRFToken': self.csrf,
        }
        params = {
            'fields': 'relations__object_type,relations__object_id,relations__params,relations_count,id,name,'
                      'pass_condition,created,campaign_ids,users,flags',
        }

        name = 'segment'

        data = {
            'name': name,
            'pass_condition': 1,
            'relations': [{
                'object_type': 'remarketing_player',
                'params': {
                    'type': 'positive',
                    'left': 365,
                    'right': 0,
                }
            }],
            'logicType': 'or',
        }

        return self.request('POST', location=location, params=params, data=json.dumps(data), headers=headers)

    def get_segments(self):
        location = 'api/v2/remarketing/segments.json'
        headers = {
            'Content-Type': 'application/json',
            'Host': 'target.my.com',
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/segments/segments_list/new',
            'X-CSRFToken': self.csrf,
        }
        params = {
            'fields': 'relations__object_type,relations__object_id,relations__params,relations_count,id,name,'
                      'pass_condition,created,campaign_ids,users,flags',
        }
        return self.request('GET', location=location, params=params, headers=headers, json=True)['items']

    def delete_segment(self, segment_id):
        location = f'api/v2/remarketing/segments/{segment_id}.json'

        headers = {
            'Host': 'target.my.com',
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/segments/segments_list',
            'X-CSRFToken': self.csrf,
        }

        return self.request('DELETE', location=location, headers=headers)

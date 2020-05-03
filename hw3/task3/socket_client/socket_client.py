import socket

import json


class SocketClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def request(self, method, url, json=False):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)
        client.connect((self.host, self.port))
        request = f"{method} {url} HTTP/1.1\r\nHost:{self.host}:{self.port}\r\n\r\n"
        client.send(request.encode())

        result_list = []
        while True:
            data = client.recv(4096)
            if data:
                result_list.append(data.decode())
            else:
                break

        client.close()

        if json:
            return self.response_to_json(''.join(result_list).splitlines())
        return ''.join(result_list)

    @staticmethod
    def response_to_json(response_list):
        result_dict = {'Status-Code': int(response_list[0].split(' ')[1])}
        for i, header in enumerate(response_list[1:]):
            if header == '':
                result_dict['Body'] = ''.join(response_list[i + 1:])
                break
            data = header.split(': ')
            result_dict[data[0]] = data[1]

        return json.dumps(result_dict)

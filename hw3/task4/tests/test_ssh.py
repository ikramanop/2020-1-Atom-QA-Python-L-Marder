import pytest
import requests


class TestSSH:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, ssh_client, config):
        self.client = ssh_client
        self.host = config['host']
        self.ssh_port = config['port']
        self.nginx_port = config['nginx_port']

    def test_root(self):
        output = self.client.execute('whoami')
        output = output.replace('\n', '')

        assert output == 'root'

    def test_nginx_ssh(self):
        output = self.client.execute("netstat -tlpn | grep nginx | awk '{print $4}'")

        assert output.split(':')[-1] != '80'

    def test_nginx_http(self):
        response = requests.get(f'http://{self.client.host}:{5478}')

        assert response.status_code == 200

    def test_nginx_log(self):
        requests.get(f'http://{self.client.host}:{self.nginx_port}')

        output = self.client.execute('cat /var/log/nginx/access.log | tail -n 1')

        log = output.replace(' - - ', ' ').replace(' / ', ' ').replace('"', '').split(' ')

        assert log[5] == '200'

    def test_no_http(self):
        self.client.execute(f'firewall-cmd --remove-port={5478}/tcp')

        with pytest.raises(requests.exceptions.ConnectionError):
            requests.get(f'http://{self.client.host}:{self.nginx_port}')

        output = self.client.execute('systemctl status nginx | grep active')

        assert output != ''

        self.client.execute('firewall-cmd --reload')

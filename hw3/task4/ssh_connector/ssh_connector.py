import time

from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, SSHException


class SSHConnector:

    def __init__(self, host, port, username, password):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password

    def __enter__(self):
        try:
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
            )
        except AuthenticationException:
            print("Authentication failed, please verify your credentials")
        except SSHException as exc:
            print(f"Could not establish SSH connection {exc}")

        return self

    def execute(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        data = stdout.read()
        data = data.decode()

        err = stderr.read()
        err = err.decode()

        if err:
            raise Exception(f'Err: {err}')

        return data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

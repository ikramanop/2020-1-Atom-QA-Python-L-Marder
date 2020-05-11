import threading

from flask import Flask, request, abort

app = Flask(__name__)

users_data = {}


def run_mock(host, port):
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    return server


def shutdown_mock():
    terminate = request.environ.get('werkzeug.server.shutdown')
    if terminate:
        terminate()


@app.route('/users/<user_id>/<user_name>', methods=['POST'])
def add_users_to_dict(user_id, user_name):
    if user_id in users_data.keys():
        abort(403)
    users_data.update({str(user_id): f'{user_name}'})
    return 'Added successfully'


@app.route('/users/<user_id>', methods=['GET'])
def get_users_by_id(user_id):
    user = users_data.get(str(user_id), None)
    if user:
        return user
    else:
        abort(404)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_mock()
    return 'Shutting down...'

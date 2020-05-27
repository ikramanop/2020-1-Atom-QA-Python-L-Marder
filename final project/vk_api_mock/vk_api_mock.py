from flask import Flask, request, json
import threading
import vk_api
from vk_api.exceptions import ApiError

app = Flask(__name__)

vk_session = vk_api.VkApi(
    token='d5d218cf9c4a1452391f88ce1aa389f7ee57b2e90c1bcbbb9d44375942ebc3ce3485a949dad71dc87b97e')
vk = vk_session.get_api()


def run_mock(host, port):
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    return server


def shutdown_mock():
    terminate = request.environ.get('werkzeug.server.shutdown')
    if terminate:
        terminate()


@app.route('/vk_id/<username>', methods=['GET'])
def get_user(username):
    try:
        result = vk.users.get(user_ids=[username])
        if 'id' in result[0]:
            response = app.response_class(
                response=json.dumps({'vk_id': result[0]['id']}),
                status=200,
                mimetype='application/json'
            )
            return response
    except ApiError:
        response = app.response_class(
            response=json.dumps({}),
            status=404,
            mimetype='application/json'
        )
        return response


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_mock()
    return 'Shutting down...'


if __name__ == '__main__':
    run_mock(host='0.0.0.0', port=5000)

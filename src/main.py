from flask import Flask
from scheduler import start_scheduler
from data.docker import dockerData
from util.decorator import api_response

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return "hello world!"


@app.route('/docker_machines', methods=['GET'])
@api_response
def docker_machines():
    return dockerData.machine_ids


@app.route('/docker_networks', methods=['GET'])
@api_response
def docker_networks():
    return dockerData.network_ids


if __name__ == '__main__':
    start_scheduler()
    app.run(debug=True, use_reloader=False)

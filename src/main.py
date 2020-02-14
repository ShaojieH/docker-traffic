from flask import Flask, render_template, redirect, url_for

from data.docker import dockerData
from scheduler import prepare
from shell.docker import get_container_interface
from shell.tc import get_current_rule, reset, limit
from util.decorator import api_response
from flask import request
app = Flask(__name__)


@app.route('/container_info', methods=['GET'])
@app.route('/', methods=['GET'])
def get_container_info():
    container_info = {}
    for container_id in dockerData.container_ids:
        interface = get_container_interface(container_id)
        container_info[container_id] = {
            "interface": interface,
            "rule": get_current_rule(interface)
        }
    return render_template('container_info.html', container_info=container_info)


@app.route('/reset_container_rule', methods=['POST'])
def reset_container_rule():
    interface = request.form['interface']
    reset(interface)
    return redirect('/')


@app.route('/set_container_rule', methods=['POST'])
def set_container_rule():
    interface = request.form['interface']
    rate = request.form['rate']
    burst = request.form['burst']
    latency = request.form['latency']
    reset(interface) # first reset anyway
    limit(interface=interface, rate=rate+"Mbit", burst=burst+"kb", latency=latency+"ms")
    return redirect('/')


if __name__ == '__main__':
    prepare()
    app.run(debug=True, use_reloader=False)

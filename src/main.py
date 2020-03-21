from flask import Flask, render_template, redirect
from flask import request

from data.docker import dockerData
from scheduler import prepare
from shell.docker import get_container_interface, get_container_ip2, get_container_name
from shell.tc import get_current_rule, reset, limit, limit_by_src_and_dst

app = Flask(__name__)


@app.route('/container_info', methods=['GET'])
@app.route('/', methods=['GET'])
def get_container_info():
    container_info = {}
    for container_id in dockerData.container_ids:
        interface = get_container_interface(container_id)
        ip = get_container_ip2(container_id)
        name = get_container_name(container_id)
        container_info[container_id] = {
            "interface": interface,
            "rule": get_current_rule(interface),
            "ip": ip,
            "name": name,
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
    reset(interface)  # first reset anyway
    limit(interface=interface, rate=rate + "Mbit", burst=burst + "kb", latency=latency + "ms")
    return redirect('/')


@app.route('/add_container_rule', methods=['POST'])
def add_container_rule():
    src_container_id = request.form['src_container_id']
    dst_container_id = request.form['dst_container_id']
    limit = request.form['limit']
    limit_by_src_and_dst(src_container_id=src_container_id, dst_container_id=dst_container_id, limit=limit)
    return redirect('/')

@app.route('add_container_rule', methods=['GET'])
def graph():
    return render_template('graph.html',)

if __name__ == '__main__':
    prepare()
    app.run(debug=True, use_reloader=False)

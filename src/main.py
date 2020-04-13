from flask import Flask, render_template, redirect
from flask import request

from data.docker import dockerData
from scheduler import prepare
from shell.config import get_docker_config_list, get_docker_config
from shell.docker import get_container_interface, get_container_ip2, get_container_name, get_container_id_by_ip
from shell.tc import get_qdisc_rule, reset, limit, limit_by_src_and_dst, get_class, get_filter, get_class_limit, \
    get_filter_src
from util.decorator import api_response
from util.web import wrap_response

app = Flask(__name__)


@app.route('/api/container_info', methods=['GET'])
@api_response
def api_get_container_info():
    container_info = []
    for container_id in dockerData.container_ids:
        interface = get_container_interface(container_id)
        ip = get_container_ip2(container_id)
        name = get_container_name(container_id)
        container_info.append({
            "data": {
                "interface": interface,
                "ip": ip,
                "name": name,
                "id": container_id,
                "class": get_class(container_id),
                "filter": get_filter(container_id),
            }
        })
        container_class_limit = get_class_limit(interface)
        if len(container_class_limit):
            container_filter_src = get_filter_src(interface)
            container_info.append({
                "data": {
                    "id": container_id + "/" + container_filter_src,
                    "source": get_container_id_by_ip(container_filter_src),
                    "target": container_id,
                    "limit": container_class_limit,
                }
            })

    return container_info


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
            "rule": get_qdisc_rule(interface),
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


@app.route('/graph', methods=['GET'])
def graph():
    return render_template('graph.html')


@app.route('/configs', methods=['GET'])
def docker_configs():
    return render_template('config_list.html', list_of_file=get_docker_config_list())


@app.route('/config/<filename>', methods=['GET'])
def docker_config(filename):
    return render_template('docker_config2.html', docker_config=get_docker_config(filename))


if __name__ == '__main__':
    prepare()
    app.run(debug=True, use_reloader=False)

from datetime import datetime

from flask import Flask, render_template, redirect
from flask import request
from flask_cors import CORS

from data.docker import dockerData
from scheduler import prepare
from shell.docker import get_container_interface, get_container_ip2, get_container_name, get_container_id_by_ip
from shell.docker_config import get_config_list, get_config, set_config, apply_config
from shell.tc import get_qdisc_rule, reset, limit, limit_by_src_and_dst, get_class, get_filter, get_class_limit, \
    get_filter_src
from util.decorator import api_response
from util.rule_apply import do_apply_simple_test, do_reset_simple_test, do_apply_complex_test, do_apply_simple, \
    do_reset_simple

app = Flask(__name__)
CORS(app)


@app.route('/api/container/graph', methods=['GET'])
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


@app.route('/api/container', methods=['GET'])
@api_response
def api_get_container_list():
    container_info = []
    for container_id in dockerData.container_ids:
        interface = get_container_interface(container_id)
        ip = get_container_ip2(container_id)
        name = get_container_name(container_id)
        container_info.append({
            "container_id": container_id,
            "interface": interface,
            "rule": get_qdisc_rule(interface),
            "ip": ip,
            "name": name,
        })
    return container_info


@app.route('/container_info', methods=['GET'])
@app.route('/', methods=['GET'])
def get_container_info():
    return render_template('container_info.html', container_info=api_get_container_list())


@app.route('/api/container/reset', methods=['POST'])
@api_response
def api_reset_container_rule():
    interface = request.form['interface']
    return reset(interface)


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


@app.route('/api/config', methods=['GET'])
def api_get_docker_config_list():
    return {'configs': get_config_list()}


@app.route('/config', methods=['GET'])
def get_docker_config_list():
    return render_template('docker_config_list.html', list_of_file=get_config_list())


@app.route('/api/config/<filename>', methods=['GET'])
def api_get_docker_config(filename):
    return get_config(filename)


@app.route('/config/<filename>', methods=['GET'])
def get_docker_config(filename):
    return render_template('docker_config.html', docker_config=get_config(filename), filename=filename)


@app.route('/config/<filename>', methods=['POST'])
def save_docker_config(filename):
    set_config(filename, request.form['content'])
    return redirect('/config/{0}'.format(filename))


@app.route('/config/apply/<filename>', methods=['POST'])
def apply_docker_config(filename):
    apply_config(filename)
    return redirect('/graph')


@app.route('/api/config/apply/<filename>', methods=['POST'])
def api_docker_config(filename):
    start = datetime.now()
    apply_config(filename)
    end = datetime.now()
    print("time", end - start)
    return "success"


@app.route('/api/test/simple/apply', methods=['POST'])
def api_apply_simple_test():
    do_apply_simple_test()
    return "success"


@app.route('/api/test/complex/apply', methods=['POST'])
def api_apply_complex_test():
    return do_apply_complex_test()
    # return "success"


@app.route('/api/test/simple/reset', methods=['POST'])
def api_reset_simple_test():
    return do_reset_simple_test()
    # return "success"


@app.route('/api/simple/apply', methods=['POST'])
def api_apply_simple():
    container = request.args.get('container')
    dst_ip = request.args.get('dst_ip')
    limit = request.args.get('limit')
    prio = request.args.get('prio')
    return do_apply_simple(container, dst_ip, limit, prio)


@app.route('/api/simple/reset', methods=['POST'])
def api_reset_simple():
    container = request.args.get('container')
    return do_reset_simple(container)


if __name__ == '__main__':
    prepare()
    app.run(debug=True, use_reloader=False)

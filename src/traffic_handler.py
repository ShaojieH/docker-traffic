from db.influx import save_bandwhich_connection_data

current_batch_time = 0
current_second_data = {}


def handle_bandwhich(traffic_info):
    global current_second_data, current_batch_time
    if current_batch_time == int(traffic_info['time']):
        if traffic_info['dst'] not in current_second_data:
            current_second_data[traffic_info['dst']] = int(traffic_info['down'])
        else:
            current_second_data[traffic_info['dst']] += int(traffic_info['down'])
    else:
        if len(current_second_data.keys()) is not 0:
            print(current_second_data, current_batch_time)
            for dst, down in current_second_data.items():
                save_bandwhich_connection_data(dst, down, current_batch_time)
        current_second_data = {}
        current_batch_time = int(traffic_info['time'])
        handle_bandwhich(traffic_info)

    # <Result () {'time': '1579016408', 'device': 'br-089d114ea447', 'device_port': '7005', 'dst': '172.18.0.5', 'dst_port': '36560', 'protocol': 'tcp', 'up': '0', 'down': '212', 'process': '<UNKNOWN>'}>

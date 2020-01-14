from db.influx import save_bandwhich_connection_data


def handle_bandwhich(traffic_info):
    # <Result () {'time': '1579016408', 'device': 'br-089d114ea447', 'device_port': '7005', 'dst': '172.18.0.5', 'dst_port': '36560', 'protocol': 'tcp', 'up': '0', 'down': '212', 'process': '<UNKNOWN>'}>
    save_bandwhich_connection_data(traffic_info)
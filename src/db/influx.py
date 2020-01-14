from influxdb import InfluxDBClient

from config import influxdb_database_name, influxdb_connection

client = InfluxDBClient(host='localhost', port=8086, username='root', password='root',
                        database=influxdb_database_name)


def save_bandwhich_connection_data(data):
    json_body = [
        {
            "measurement": influxdb_connection,
            # "time": int(data['time']),
            "tags": {
                "device": data['device'],
                "dst": data['dst'],
                "protocol": data['protocol'],
            },
            "fields": {
                "down": int(data['down']),
            }
        }
    ]
    # print(json_body)
    client.write_points(json_body, time_precision='s')


if __name__ == '__main__':
    result = client.query("select * from {0};".format(influxdb_connection))
    print(result)

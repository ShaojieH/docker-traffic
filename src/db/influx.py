from influxdb import InfluxDBClient

from config import influxdb_database_name, influxdb_connection, influxdb_address

client = InfluxDBClient(host=influxdb_address, port=8086, username='root', password='root',
                        database=influxdb_database_name)


def save_bandwhich_connection_data(dst, down, time):
    json_body = [
        {
            "measurement": influxdb_connection,
            "time": int(time),
            "tags": {
                # "device": data['device'],
                "dst": dst,
                # "protocol": data['protocol'],
            },
            "fields": {
                "down": down,
            }
        }
    ]
    # print(json_body)
    client.write_points(json_body, time_precision='s')


if __name__ == '__main__':
    # save_bandwhich_connection_data('172.18.0.5', 0, '1581494417')
    result = client.query("select * from {0};".format(influxdb_connection))
    print(result)

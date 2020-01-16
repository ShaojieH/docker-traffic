import threading
from time import sleep

from data.docker import dockerData
from traffic_handler import handle_bandwhich
from util.shell import sudo_run_and_get_realtime_result
from util.traffic_parse import match_bandwhich_output, Traffic_log_type


def start_bandwhich_monitor():
    download_thread = threading.Thread(target=do_start_bandwhich_monitor)
    download_thread.start()


def do_start_bandwhich_monitor():
    # default_device = "br-089d114ea447"
    while not dockerData or not dockerData.network_ids or len(dockerData.network_ids) == 0:
        sleep(1)
    print("start capturing traffic with bandwhich")
    default_device = "br-{0}".format(dockerData.network_ids[0])
    command = "/home/houshaojie/.cargo/bin/bandwhich -n -r -i {0}".format(default_device)
    process = sudo_run_and_get_realtime_result(command)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll():
            break
        else:
            traffic_log_type, traffic_info = match_bandwhich_output(output.decode("utf-8"))
            if traffic_log_type == Traffic_log_type.BANDWHICH_CONNECTION:
                handle_bandwhich(traffic_info)

if __name__ == '__main__':
    do_start_bandwhich_monitor()

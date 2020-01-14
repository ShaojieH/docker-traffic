from data.docker import dockerData
from util.shell import sudo_run_and_get_result


def docker_ps():
    command = 'docker ps -q'
    result = sudo_run_and_get_result(command).split()
    dockerData.machine_ids = result


def docker_network_ls():
    command = 'docker network ls --filter type=custom -q'
    result = sudo_run_and_get_result(command).split()
    dockerData.network_ids = result
    # default_interface = "br-{0}".format(result[0])
    # print(default_interface)

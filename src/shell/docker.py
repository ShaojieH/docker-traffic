from data.docker import dockerData
from util.shell import sudo_run_and_get_result, sudo_run_and_get_result_or_error


def docker_ps():
    command = 'docker ps -q'
    result = sudo_run_and_get_result(command).split()
    dockerData.container_ids = result


def docker_network_ls():
    command = 'docker network ls --filter type=custom -q'
    result = sudo_run_and_get_result(command).split()
    dockerData.network_ids = result
    # default_interface = "br-{0}".format(result[0])
    # print(default_interface)


def get_container_interface(container_id):
    command = "./shell/get_interface.sh {0}".format(container_id)
    result = sudo_run_and_get_result_or_error(command)
    return result.split("@")[0]


if __name__ == '__main__':
    get_container_interface("fe04af677676")

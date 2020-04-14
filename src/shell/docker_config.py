import yaml

from config import DOCKER_CONFIG_DIR, DOCKER_DIR, DOCKER_COMPOSE
from data.docker import dockerData
from shell.docker import docker_ps, docker_network_ls, get_container_id_by_name
from shell.tc import limit_by_src_and_dst
from util.shell import sudo_run_and_get_result, sudo_run_and_get_realtime_result


def get_config_list():
    result = sudo_run_and_get_result("ls {0}".format(DOCKER_CONFIG_DIR))
    return result.split()


def get_config(filename):
    with open(DOCKER_CONFIG_DIR + "/" + filename) as file:
        lines = file.readlines()
        result = "".join(lines)
        return result


def set_config(filename, content):
    with open(DOCKER_CONFIG_DIR + "/" + filename, 'r+') as file:
        file.seek(0)
        file.write(content)
        file.truncate()


def apply_config(filename):
    with open(DOCKER_CONFIG_DIR + "/" + filename) as file:
        config = yaml.load(file, yaml.FullLoader)
        worker_count = config['worker']
        init_container(worker_count)
        speed_limits = config['speed_limit']
        for speed_limit in speed_limits:
            from_container = speed_limit['from_container']
            from_container_id = get_container_name_mapping(from_container)
            to_container = speed_limit['to_container']
            to_container_id = get_container_name_mapping(to_container)
            limit = speed_limit['limit']
            limit_by_src_and_dst(from_container_id, to_container_id, limit)


def init_container(worker_count):
    command = DOCKER_DIR + "/deploy.sh {0} {1}".format(worker_count, DOCKER_COMPOSE)
    process = sudo_run_and_get_realtime_result(command)
    while True:
        output = process.stdout.readline()
        if output == b'':
            break
        else:
            print(output)

    docker_ps()
    docker_network_ls()


def get_container_name_mapping(config_name: str):  # "worker_{id}" or "master"
    if config_name == "master":
        container_name = "/docker-spark_master_1"
    else:
        worker_index = int(config_name.split("_")[-1])
        container_name = "/docker-spark_worker_{0}".format(worker_index)

    return get_container_id_by_name(container_name)


def main():
    apply_config("test.yml")


if __name__ == '__main__':
    main()

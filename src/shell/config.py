from config import DOCKER_CONFIG_DIR
from util.shell import sudo_run_and_get_result


def get_docker_config_list():
    result = sudo_run_and_get_result("ls {0}".format(DOCKER_CONFIG_DIR))
    return result.split()


def get_docker_config(filename):
    with open(DOCKER_CONFIG_DIR + "/" + filename) as file:
        lines = file.readlines()
        result = "".join(lines)
        print(result)
        return result

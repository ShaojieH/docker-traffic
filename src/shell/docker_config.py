import yaml

from config import DOCKER_CONFIG_DIR, DOCKER_DIR, DOCKER_COMPOSE
from shell.docker import docker_ps, docker_network_ls, get_container_id_by_name
from util.shell import sudo_run_and_get_result, sudo_run_and_get_realtime_result

GROUP_TYPE = 1
CONTAINER_TYPE = 2
ROOT_TYPE = 2


class TreeNode:
    name: str
    children: []
    limit: int
    node_type: int

    def __init__(self, name: str, node_type: int):
        self.name = name
        self.node_type = node_type
        self.children = []
        self.limit = 0

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.name) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def find_by_name(self, name):
        if self.name == name:
            return self

        for child in self.children:
            result = child.find_by_name(name)
            if result:
                return result
        return None


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


def get_node_type(name):
    if "worker" in name:
        return CONTAINER_TYPE
    else:
        return GROUP_TYPE


def apply_config(filename):
    with open(DOCKER_CONFIG_DIR + "/" + filename) as file:
        config = yaml.load(file, yaml.FullLoader)
        worker_count = config['worker']
        containers = []
        for count in range(1, worker_count + 1):
            containers.append(f"worker_{count}")
        # init_container(worker_count)
        speed_limits = config['speed_limit']
        groups = config['groups']
        root = TreeNode("root", ROOT_TYPE)

        added_groups = [root]
        added_containers = []
        for group in groups:
            for added_group in added_groups:
                if added_group.name == group['parent']:
                    node = TreeNode(group['name'], GROUP_TYPE)
                    for child in group['children']:
                        node_type = get_node_type(child)
                        if node_type is CONTAINER_TYPE:
                            node.children.append(TreeNode(child, CONTAINER_TYPE))
                            added_containers.append(child)
                    added_groups.append(node)
                    added_group.children.append(node)
                    break

        for container in containers:
            if container not in added_containers:
                added_containers.append(container)
                root.children.append(TreeNode(container, CONTAINER_TYPE))

        print(root)

        for speed_limit in speed_limits:
            to_container = speed_limit['to_container']
            node = root.find_by_name(to_container)
            node.limit = speed_limit['limit']
            # print(to_container)
            # print(node.name)
        # for speed_limit in speed_limits:
        #     from_container = speed_limit['from_container']
        #     from_container_id = get_container_name_mapping(from_container)
        #     to_container = speed_limit['to_container']
        #     to_container_id = get_container_name_mapping(to_container)
        #     limit = speed_limit['limit']
        #     limit_by_src_and_dst(from_container_id, to_container_id, limit)


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


if __name__ == '__main__':
    apply_config("test2.yml")

import time

import yaml

from config import DOCKER_CONFIG_DIR, DOCKER_DIR, DOCKER_COMPOSE
from data.docker import dockerData
from shell.docker import get_container_id_by_name, get_container_ip
from util.shell import sudo_run_and_get_result, sudo_run_and_get_realtime_result, sudo_run_and_get_result_or_error

GROUP_TYPE = 1
CONTAINER_TYPE = 2
ROOT_TYPE = 2


class TreeNode:
    name: str
    children: []
    limit: int
    prio: int
    node_type: int
    x: int
    parent: str
    real_children: []

    def __init__(self, name: str, node_type: int):
        self.name = name
        self.node_type = node_type
        self.children = []
        self.limit = 0
        self.prio = 0
        self.parent = ""
        self.real_children = []

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


def compute_real_children(group):
    for child in group.children:
        if get_node_type(child.name) == CONTAINER_TYPE:
            group.real_children.append(child)
        else:
            compute_real_children(child)
            group.real_children.extend(child.real_children)


def apply_config(filename):
    with open(DOCKER_CONFIG_DIR + "/" + filename) as file:
        config = yaml.load(file, yaml.FullLoader)
        worker_count = config['worker']
        containers = []
        for count in range(1, worker_count + 1):
            containers.append(f"worker_{count}")
        commands = []
        for rule in config['rules']:
            root_container = rule['root']
            speed_limits = rule['speed_limits']
            root_container_id = get_container_name_mapping(root_container)
            commands.append(qdisc_del(root_container_id))

            groups = rule['groups'] if 'groups' in rule else []
            root = TreeNode("root", ROOT_TYPE)
            root.parent = "root"

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

            compute_real_children(root)

            for speed_limit in speed_limits:
                to_container = speed_limit['to_container']
                node = root.find_by_name(to_container)
                node.limit = speed_limit['limit']
                node.prio = speed_limit['prio']

            x = 1
            for group in added_groups:
                group.x = x
                x = x * 10
                handle = f"{group.x}:0"
                class_id = f"{group.x}:1"
                commands.append(qdisc_add(group.parent, handle, root_container_id))
                commands.append(default_add(class_id, group.x, root_container_id))
                commands.append(class_add(handle, class_id, 99999, root_container_id))

                y = 10

                for child in group.children:
                    limit = None
                    for speed_limit in speed_limits:
                        to_container = speed_limit['to_container']
                        if child.name == to_container:
                            limit = speed_limit['limit']
                            prio = speed_limit['prio']
                            break
                    if not limit:
                        continue
                    child_classid = f"{group.x}:{y}"
                    child.parent = child_classid
                    child.class_id = child_classid
                    y = y + 1
                    commands.append(class_add(class_id, child_classid, limit, root_container_id, prio))

                    if get_node_type(child.name) == CONTAINER_TYPE:
                        container_id = get_container_name_mapping(child.name)
                        ip = get_container_ip(container_id)
                        commands.append(filter_add(handle, ip, child.parent, root_container_id))

                    elif get_node_type(child.name) == GROUP_TYPE:
                        for real_child in child.real_children:
                            container_id = get_container_name_mapping(real_child.name)
                            ip = get_container_ip(container_id)
                            commands.append(filter_add(handle, ip, child_classid, root_container_id))

        init_container(worker_count)
        for command in commands:
            print(command)
            sudo_run_and_get_result_or_error(command)


def qdisc_del(container_id):
    return f"docker exec {container_id} tc qdisc del dev eth0 root"


def qdisc_add(parent: str, handle: str, container_id: str):
    return f"docker exec {container_id} tc qdisc add dev eth0 parent {parent} handle {handle} htb default 22"


def default_add(parent: str, x, container_id: str):
    return f"docker exec {container_id} tc class add dev eth0 parent {parent} classid {x}:22 htb rate 99999kbps ceil 99999kbps"


def class_add(parent: str, classid: str, limit: int, container_id: str, prio=0):
    return f"docker exec {container_id} tc class add dev eth0 parent {parent} classid {classid} htb rate {limit}kbps ceil {limit}kbps prio {prio}"


def filter_add(parent: str, ip: str, flowid: str, container_id: str):
    return f"docker exec {container_id} tc filter add dev eth0 protocol ip parent {parent} prio 1 u32 match ip dst {ip} flowid {flowid}"


def init_container(worker_count):
    if len(dockerData.container_ids) == worker_count + 1:
        return
    command = DOCKER_DIR + "/deploy.sh {0} {1}".format(worker_count, DOCKER_COMPOSE)
    process = sudo_run_and_get_realtime_result(command)
    while True:
        output = process.stdout.readline()
        if output == b'':
            break
        else:
            print(output)

    while len(dockerData.container_ids) != worker_count + 1:
        time.sleep(1)


def get_container_name_mapping(config_name: str):  # "worker_{id}" or "master"
    if config_name == "master":
        container_name = "/docker-spark_master_1"
    else:
        worker_index = int(config_name.split("_")[-1])
        container_name = "/docker-spark_worker_{0}".format(worker_index)

    return get_container_id_by_name(container_name)

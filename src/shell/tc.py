from shell.docker import get_container_interface, get_container_ip
from util.shell import sudo_run_and_get_result, sudo_run_and_get_result_or_error
from util.tc import get_src_by_filter, get_limit_by_class


def get_qdisc_rule(interface):
    command = "tc qdisc show dev {0}".format(interface)
    result = sudo_run_and_get_result(command)
    return result


def get_class_limit(interface):
    return get_limit_by_class(get_class(interface))


def get_class(interface):
    command = "tc class show dev {0}".format(interface)
    result = sudo_run_and_get_result(command)
    return result


def get_filter_src(interface):
    return get_src_by_filter(get_filter(interface))


def get_filter(interface):
    command = "tc filter show dev {0}".format(interface)
    result = sudo_run_and_get_result(command)
    return result


def reset(interface):
    command = "tc qdisc del dev {0} root".format(interface)
    result = sudo_run_and_get_result_or_error(command)
    print(result)
    return {"result": result}


def limit(interface, rate="4Mbit", burst="10kB", latency="1000ms"):
    command = "sudo tc qdisc add dev {0} root tbf rate {1} burst {2} latency {3}".format(interface, rate, burst,
                                                                                         latency)
    result = sudo_run_and_get_result_or_error(command)
    print(result)
    return {"result": result}


def limit_by_src_and_dst(src_container_id, dst_container_id, limit=5000):
    """

    :param src_container_id:
    :param dst_container_id:
    :param limit: kB
    """
    dst_container_interface = get_container_interface(dst_container_id)
    src_container_ip = get_container_ip(src_container_id)
    command = "./shell/tc_by_ip_2.sh {0} {1} {2}".format(dst_container_interface, src_container_ip, limit)
    # print(command)
    result = sudo_run_and_get_result_or_error(command)
    # print(result)
    return {"result": result}


if __name__ == '__main__':
    # limit(device="veth35aab1b", rate="10Mbit", burst="500kB", latency="10s")
    print(get_class("veth073869f"))
    # limit("br-089d114ea447")
    # reset("br-089d114ea447")fe04af677676
    # limit_by_src_and_dst("7340cd9db3f9", "fe04af677676", 10000)

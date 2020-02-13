from util.shell import sudo_run_and_get_result, sudo_run_and_get_result_or_error


def get_current_rule(interface):
    command = "tc qdisc show dev {0}".format(interface)
    result = sudo_run_and_get_result(command)
    return result


def reset(interface):
    command = "tc qdisc del dev {0} root".format(interface)
    result = sudo_run_and_get_result_or_error(command)
    print(result)


def limit(interface, rate="4Mbit", burst="10kB", latency="1000ms"):
    command = "sudo tc qdisc add dev {0} root tbf rate {1} burst {2} latency {3}".format(interface, rate, burst, latency)
    result = sudo_run_and_get_result_or_error(command)
    print(result)


if __name__ == '__main__':
    # limit(device="veth35aab1b", rate="10Mbit", burst="500kB", latency="10s")
    reset("veth35aab1b")
    # limit("br-089d114ea447")
    # reset("br-089d114ea447")

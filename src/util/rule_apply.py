from util.shell import sudo_run_and_get_result_or_error


def do_apply_simple_test():
    command = "./shell/apply_simple_test.sh"
    result = sudo_run_and_get_result_or_error(command)
    print(result)
    return result


def do_apply_simple(container, ip, limit, prio):
    command = f"./shell/apply_simple.sh {container} {ip} {limit} {prio}"
    result = sudo_run_and_get_result_or_error(command)
    print(result)
    return result


def do_reset_simple(container):
    command = f"./shell/reset_simple.sh {container}"
    result = sudo_run_and_get_result_or_error(command)
    print(result)
    return result


def do_apply_complex_test():
    command = "./shell/apply_complex_test.sh"
    result = sudo_run_and_get_result_or_error(command)
    print(result)
    return result


def do_reset_simple_test():
    command = "./shell/reset_simple_test.sh"
    result = sudo_run_and_get_result_or_error(command)
    print(result)
    return result

import shlex
import subprocess

from config import sudoPassword


def get_sudo_command(command):
    return 'echo %s | sudo -S %s' % (sudoPassword, command)


def run_and_get_result(command):
    command_arr = command.split()
    return subprocess.run([command_arr], capture_output=True)
    # return os.popen(command).read()


def sudo_run_and_get_result(command):
    echo = subprocess.Popen(['echo', sudoPassword], stdout=subprocess.PIPE)
    process = subprocess.run(['sudo', '-S'] + command.split(), stdin=echo.stdout, capture_output=True)
    return process.stdout.decode("utf-8")


def sudo_run_and_get_result_or_error(command):
    echo = subprocess.Popen(['echo', sudoPassword], stdout=subprocess.PIPE)
    process = subprocess.run(['sudo', '-S'] + command.split(), stdin=echo.stdout, capture_output=True)
    result = process.stdout.decode("utf-8")
    if len(result) == 0:
        error = process.stderr.decode("utf-8")
        return error
    return result


def sudo_run_and_get_realtime_result(command):
    echo = subprocess.Popen(['echo', sudoPassword], stdout=subprocess.PIPE)
    process = subprocess.Popen(['sudo', '-S'] + shlex.split(command), stdin=echo.stdout, stdout=subprocess.PIPE)
    return process

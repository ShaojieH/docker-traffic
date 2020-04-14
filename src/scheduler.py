from apscheduler.schedulers.background import BackgroundScheduler

from config import docker_ps_interval, docker_network_ls_interval
from shell.docker import docker_ps, docker_network_ls
from shell.bandwhich import start_bandwhich_monitor

background_scheduler = BackgroundScheduler()


def prepare():
    start_scheduler()
    start_bandwhich_monitor()


def start_scheduler():
    background_scheduler.add_job(docker_ps, 'interval', seconds=docker_ps_interval)
    background_scheduler.add_job(docker_network_ls, 'interval', seconds=docker_network_ls_interval)
    background_scheduler.start()

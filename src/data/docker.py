from typing import List


class DockerData:
    machine_ids: List[str]
    network_ids: List[str]

    def __init__(self):
        self.machine_ids = []
        self.network_ids = []


dockerData = DockerData()

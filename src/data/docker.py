from typing import List


class DockerData:
    container_ids: List[str]
    network_ids: List[str]

    def __init__(self):
        self.container_ids = []
        self.network_ids = []


dockerData = DockerData()

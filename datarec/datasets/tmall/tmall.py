from datarec.datasets.tmall.tmall_v1 import Tmall_v1


class Tmall:
    latest_version = 'v1'

    def __new__(self, version: str = 'latest', **kwargs):

        versions = {'v1': Tmall_v1}
        if version == 'latest':
            version = self.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Tmall dataset: Unsupported version")

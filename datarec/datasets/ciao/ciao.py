from datarec.datasets.ciao.ciao_v1 import Ciao_V1


class Ciao:
    latest_version = 'v1'
    def __new__(self, version: str = 'latest', **kwargs):

        versions = {'v1': Ciao_V1}
        if version == 'latest':
            version = self.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Ciao: Unsupported version")

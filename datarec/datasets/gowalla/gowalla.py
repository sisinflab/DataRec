from datarec.datasets.gowalla.gowalla_v1 import Gowalla_V1


class Gowalla:
    latest_version = 'v1'
    def __new__(self, version: str = 'latest', **kwargs):

        versions = {'v1': Gowalla_V1}
        if version == 'latest':
            version = self.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Gowalla: Unsupported version")

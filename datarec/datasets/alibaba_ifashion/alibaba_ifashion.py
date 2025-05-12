from datarec.datasets.alibaba_ifashion.alibaba_ifashion_v1 import AlibabaIFashion_V1


class AlibabaIFashion:
    latest_version = 'v1'

    def __new__(cls, version: str = 'latest', **kwargs):
        versions = {'v1': AlibabaIFashion_V1}
        if version == 'latest':
            version = cls.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Alibaba iFashion: Unsupported version")

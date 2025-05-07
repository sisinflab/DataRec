from datarec.datasets.yelp.yelp_v1 import Yelp_v1


class Yelp:
    latest_version = 'v1'

    def __new__(self, version: str = 'latest', **kwargs):

        versions = {'v1': Yelp_v1}
        if version == 'latest':
            version = self.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Yelp dataset: Unsupported version")

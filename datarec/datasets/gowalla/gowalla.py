from datarec.datasets.gowalla.gowalla_friendships import GowallaFriendships
from datarec.datasets.gowalla.gowalla_checkins import GowallaCheckins


class Gowalla:
    latest_version = 'checkins'

    def __new__(self, version: str = 'latest', **kwargs):

        versions = {'friendships': GowallaFriendships,
                    'checkins': GowallaCheckins}
        if version == 'latest':
            version = self.latest_version
        if version in versions:
            return versions[version]()
        else:
            raise ValueError("Gowalla: Unsupported version")

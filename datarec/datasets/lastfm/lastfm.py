from datarec.datasets.lastfm.lastfm_2011 import LastFM2011


class LastFM:
    VERSIONS = {'2011': LastFM2011}
    latest_version = '2011'

    def __new__(cls, version: str = 'latest', **kwargs):

        if version == 'latest':
            version = cls.latest_version
        if version in cls.VERSIONS:
            return cls.VERSIONS[version]()
        else:
            raise ValueError(f"HetRec LastFM {version}: Unsupported version \n Supported version:"
                             f"\n \t version \t name "
                             f"\n \t 2011 \t LastFM (HetRec) 2011")

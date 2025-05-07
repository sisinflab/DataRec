from datarec.datasets.mind.mindLarge import MindLarge
from datarec.datasets.mind.mindSmall import MindSmall


class Mind:
    latest_version = 'large'
    versions = {'large': MindLarge,
                'small': MindSmall}


    def __new__(cls, version: str = 'latest', split: str = 'train', **kwargs):

        if version == 'latest':
            version = cls.latest_version
        if version in cls.versions:
            return cls.versions[version](split=split)
        else:
            raise ValueError("Mind dataset: Unsupported version")

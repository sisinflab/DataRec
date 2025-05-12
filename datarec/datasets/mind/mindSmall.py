import os
from datarec.data.dataset import DataRec
from datarec.io import RawData
from datarec.io.paths import dataset_directory, RAW_DATA_FOLDER
from datarec.datasets.download import decompress_zip_file
from datarec.io.readers import read_inline
from datarec.data.utils import verify_checksum
from datarec.datasets.mind.mindLarge import MindLarge


class MindSmall(MindLarge):

    REQUIRED = {
        'train': {
            'compressed': 'MINDsmall_train.zip',
            'decompressed': ['behaviors.tsv', 'entity_embedding.vec', 'relation_embedding.vec', 'news.tsv'],
            'interactions': 'behaviors.tsv',
            'checksum': '8ab752c7d11564622d93132be05dcf6b'
        },
        'validation': {
            'compressed': 'MINDsmall_dev.zip',
            'decompressed': ['behaviors.tsv', 'entity_embedding.vec', 'relation_embedding.vec', 'news.tsv'],
            'interactions': 'behaviors.tsv',
            'checksum': 'e3bac5485be8fc7a9934e85e3b78615f'
        }
    }

    SPLITS = ('train', 'validation')

    VERSION = 'small'

    def __init__(self, folder=None, split='train'):

        super().__init__(folder=folder, split=split)


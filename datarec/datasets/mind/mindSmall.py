"""Builder class for the small version of the MIND dataset."""
import os
from datarec.data.dataset import DataRec
from datarec.io import RawData
from datarec.io.paths import dataset_directory, RAW_DATA_FOLDER
from datarec.datasets.download import decompress_zip_file
from datarec.io.readers import read_inline
from datarec.data.utils import verify_checksum
from datarec.datasets.mind.mindLarge import MindLarge


class MindSmall(MindLarge):
    """
    Builder class for the small version of the MIND dataset.

    This class handles the logic for preparing and loading the MINDsmall dataset.
    It inherits most of its functionality from the `MindLarge` class but overrides
    the required file configurations for the smaller version.

    MINDsmall is a smaller version of the MIND dataset, suitable for rapid
    prototyping. It contains only `train` and `validation` splits.

    **Note on usage:** Like the large version, this dataset requires manual download.

    Attributes:
        REQUIRED (dict): A dictionary detailing the filenames and checksums for
            each data split (train, validation).
        SPLITS (tuple): The available splits for this version.
    """

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
        """
        Initializes the builder for the MINDsmall dataset.

        This constructor calls the parent `MindLarge` constructor but will use the
        overridden `REQUIRED`, `SPLITS`, and `VERSION` attributes specific to
        the small version of the dataset.

        Args:
            folder (str, optional): A custom directory to store the dataset files.
                If None, a default user cache directory is used. Defaults to None.
            split (str, optional): The data split to load, one of 'train' or
                'validation'. Defaults to 'train'.
        """

        super().__init__(folder=folder, split=split)


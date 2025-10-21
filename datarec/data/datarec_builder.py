from abc import ABC, abstractmethod
from datarec.data.dataset import DataRec
from datarec.io.paths import dataset_directory, dataset_raw_directory, RAW_DATA_FOLDER
import os

class BaseDataRecBuilder(ABC):
    """
    Abstract base class for building `DataRec` datasets.

    This class defines the interface for preparing, downloading, and loading 
    datasets into `DataRec` objects. 
    """
    dataset_name: str
    version: str

    @abstractmethod
    def prepare(self) -> None:
        """Download and process the dataset, without loading it into memory."""
        pass

    @abstractmethod
    def load(self) -> DataRec:
        """Load the processed dataset into a DataRec object."""
        pass

    def prepare_and_load(self) -> DataRec:
        """
        A convenience method that runs the full prepare and load pipeline.

        Returns:
            (DataRec): The fully prepared and loaded dataset.
        """
        self.prepare()
        return self.load()

    @abstractmethod
    def download(self) -> str:
        """Download the raw dataset files."""
        pass

    def download_content(self) -> str:
        """Download the raw content files."""
        pass

    def find_output_folder(self, folder=None) -> str:
        """
        Find the output folder for the given dataset and version.
        Args:
            folder (str): Explicit output folder path.
        Returns:
            (str): The output folder path.
        """
        if folder:
            return os.path.abspath(os.path.join(folder, RAW_DATA_FOLDER))
        return os.path.join(dataset_raw_directory(self.dataset_name), self.version)


from abc import ABC, abstractmethod
from datarec.data.dataset import DataRec


class BaseDataRecBuilder(ABC):
    """
    Abstract base class for building `DataRec` datasets.

    This class defines the interface for preparing, downloading, and loading 
    datasets into `DataRec` objects. 
    """
    
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

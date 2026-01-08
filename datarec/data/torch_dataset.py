import torch
from torch.utils.data import Dataset
import numpy as np
from typing import Any, List


class BaseTorchDataset(Dataset):
    """
    Base class for Torch datasets wrapping a DataRec dataset.
    """
    def __init__(self, datarec, copy_data=False):
        """
        Initializes the BaseTorchDataset object.    
        
        Args:
            datarec (DataRec): An instance of a DataRec dataset.
            copy_data (bool): Whether to copy the dataset or use it by reference.
        """
        self.df = datarec.data.copy() if copy_data else datarec.data
        self.user_col = datarec.user_col
        self.item_col = datarec.item_col


class PointwiseTorchDataset(BaseTorchDataset):
    """
    Torch dataset for pointwise recommendation tasks.
    """
    def __init__(self, datarec, copy_data=False):
        """
        Initializes the PointwiseTorchDataset object.

        Args:
            datarec (DataRec): An instance of a DataRec dataset.
            copy_data (bool): Whether to copy the dataset or use it by reference.
        """
        super().__init__(datarec, copy_data)
        self.rating_col = datarec.rating_col

    def __len__(self):
        """
        Returns the total number of samples in the dataset.

        This is required by PyTorch's DataLoader to iterate over the dataset.
        
        Returns:
            (int): Number of samples in the dataset.
        """
        return len(self.df)

    def __getitem__(self, idx):
        """
        Returns a sample with user, item, and rating.
        
        Args:
            idx (int): Sample index to be returned.

        Returns:
            (dict): Sample with user, item, and rating.
        """
        row = self.df.iloc[idx]
        return {
            "user": row[self.user_col],
            "item": row[self.item_col],
            "rating": row.get(self.rating_col, 1.0)
        }


class PairwiseTorchDataset(BaseTorchDataset):
    """
    Torch dataset for pairwise recommendation tasks with negative sampling.
    """
    def __init__(self, datarec, num_negatives=1, item_pool=None, copy_data=False):
        """ 
        Initializes the PairwiseTorchDataset object.
        
        Args:
            datarec (DataRec): An instance of a DataRec dataset.
            num_negatives (int): Number of negative samples to generate per interaction.
            item_pool (array-like): Pool of items to sample from. Defaults to all items in the dataset.
            copy_data (bool): Whether to copy the dataset or use it by reference.
        """
        super().__init__(datarec, copy_data)
        self.num_negatives = num_negatives
        self.item_pool = item_pool or self.df[self.item_col].unique()
        self.user_pos_items = self.df.groupby(self.user_col)[self.item_col].apply(set).to_dict()

    def sample_negatives(self, user: Any) -> List[Any]:
        """
        Samples negative items for a given user, avoiding known positive items.

        This method is designed to be overridden to implement custom negative
        sampling strategies (e.g., popularity-based, adversarial, or
        distribution-aware sampling). The default implementation draws
        uniformly from the item pool, excluding items the user has already interacted with.

        Args:
            user: The user ID for which to sample negatives.

        Returns:
            (List): List of sampled negative item IDs.
        """
        neg_items = []
        user_positives = self.user_pos_items.get(user, set())
        while len(neg_items) < self.num_negatives:
            candidate = np.random.choice(self.item_pool)
            if candidate not in user_positives:
                neg_items.append(candidate)
        return neg_items

    def __len__(self):
        """
        Returns the total number of samples in the dataset.

        This is required by PyTorch's DataLoader to iterate over the dataset.
        
        Returns:
            (int): number of samples in the dataset.
        """
        return len(self.df)

    def __getitem__(self, idx):
        """
        Returns a sample with user, positive item, and negative items.
        
        Args:
            idx (int): Sample index to be returned.
        
        Returns:
            (dict): Sample with user, positive item, and negative items.
        """
        row = self.df.iloc[idx]
        user = row[self.user_col]
        pos_item = row[self.item_col]
        neg_items = self.sample_negatives(user)
        return {
            "user": user,
            "pos_item": pos_item,
            "neg_items": neg_items
        }


class RankingTorchDataset(BaseTorchDataset):
    """
    Torch dataset for full softmax-style ranking tasks.
    """
    def __init__(self, datarec, copy_data=False):
        """
        Initializes the RankingTorchDataset object.
        
        Args:
            datarec (DataRec): An instance of a DataRec dataset.
            copy_data (bool): Whether to copy the dataset or use it by reference.
        """
        super().__init__(datarec, copy_data)
        # Could prepare user->items mapping here for evaluation

    def __len__(self):
        """
        Returns the total number of samples in the dataset.

        This is required by PyTorch's DataLoader to iterate over the dataset.
        
        Returns:
            (int): Number of samples in the dataset.
        """
        return len(self.df)

    def __getitem__(self, idx):
        """
        Returns a sample with user and item.

        Args:
            idx (int): Sample index to be returned.
        
        Returns:
            (dict): Sample with user and item data.
        """
        row = self.df.iloc[idx]
        return {
            "user": row[self.user_col],
            "item": row[self.item_col]
            # No target — implicit ranking
        }

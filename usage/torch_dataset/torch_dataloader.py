"""
Example usage of DataRec with PyTorch's DataLoader using a pairwise task.

This script demonstrates how to:
1. Load the MovieLens 1M dataset using DataRec.
2. Convert the dataset into a pairwise PyTorch-compatible dataset.
3. Wrap it in a DataLoader and iterate over batches.
"""

from datarec.datasets import MovieLens
from torch.utils.data import DataLoader

if __name__ == '__main__':
    dr = MovieLens(version='1m')
    torch_dataset = dr.to_torch_dataset(task="pairwise")
    loader = DataLoader(torch_dataset, batch_size=100, shuffle=True)

    for i, batch in enumerate(loader):
        print(f"Batch {i + 1}")
        print(batch)

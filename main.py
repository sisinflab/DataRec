from datarec.datasets import MovieLens

dataset = MovieLens('latest')

print(f"Dataset Name: {dataset.dataset_name}")
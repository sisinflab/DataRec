from datarec.datasets import load_dataset_from_url


REGISTRY_URL = "https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/registry/versions/movielens_100k.yml"

datarec = load_dataset_from_url(REGISTRY_URL)
print(datarec)

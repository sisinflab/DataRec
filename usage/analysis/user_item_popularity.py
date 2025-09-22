from datarec.datasets import MovieLens


data = MovieLens(version='1m')

for k, v in data.users_popularity().items():
    print(k)
    print(v)

for k, v in data.items_popularity().items():
    print(k)
    print(v)

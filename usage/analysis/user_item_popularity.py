from datarec.datasets import MovieLens1M


data = MovieLens1M()

for k, v in data.users_popularity().items():
    print(k)
    print(v)

for k, v in data.items_popularity().items():
    print(k)
    print(v)

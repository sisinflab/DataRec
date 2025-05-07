from datarec.datasets import MovieLens1M


data = MovieLens1M()

print(data.users_relative_frequency())
print(data.items_relative_frequency())
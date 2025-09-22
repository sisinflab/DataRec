from datarec.datasets import MovieLens


data = MovieLens(version='1m')

print(data.users_relative_frequency())
print(data.items_relative_frequency())
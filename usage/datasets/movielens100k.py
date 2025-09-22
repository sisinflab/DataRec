from datarec.datasets import MovieLens

dr = MovieLens(version='100k').prepare_and_load()
print(dr)

db = MovieLens(version='100k')
print()


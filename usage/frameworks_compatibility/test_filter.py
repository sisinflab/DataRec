from datarec.datasets import MovieLens1M

from datarec.processing.binarizer import Binarize
from datarec.processing.kcore import UserKCore, ItemKCore, UserItemNRoundsKCore, UserItemIterativeKCore

datarec = MovieLens1M()
print(datarec)

binarizer = Binarize(threshold=3)
results = binarizer.run(datarec)

print('core user 30')
corer = UserKCore(core=30)
results = corer.run(datarec)

print(results)

print('core item 30')
corer = ItemKCore(core=30)
results = corer.run(datarec)
print(results)

print('iterative 30 30')
corer = UserItemIterativeKCore(cores=30)
results = corer.run(datarec)
print(results)

print('round 30 30')
corer = UserItemNRoundsKCore(cores=30, rounds=2)
results = corer.run(datarec)
print(results)

print('iterative 30 0')
corer = UserItemIterativeKCore(cores=[30, 0])
results = corer.run(datarec)
print(results)

print(datarec)

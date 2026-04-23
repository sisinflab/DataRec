from datarec.splitters.user_stratified.hold_out import UserStratifiedHoldOut
from datarec.datasets import AmazonCDAndVinyl
from datarec.processing.kcore import UserItemIterativeKCore
from datarec.processing.binarizer import Binarize
from datarec.splitters.user_stratified.hold_out import UserStratifiedHoldOut
from datarec.io.writers import write_transactions_tabular as write_tabular


data = AmazonCDAndVinyl(version="2014").prepare_and_load()


binarizer = Binarize(threshold=3, keep='positive')
dataset = binarizer.run(datarec=data)

kcore = UserItemIterativeKCore(cores=[5, 5])
dataset = kcore.run(dataset)

spl = UserStratifiedHoldOut(test_ratio=0.2, val_ratio=0.1)

print(spl.run(dataset))


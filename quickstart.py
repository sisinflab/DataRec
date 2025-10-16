from datarec.datasets import AmazonOffice
from datarec.processing import FilterOutDuplicatedInteractions, UserItemIterativeKCore
from datarec.splitters import RandomHoldOut

# 1️⃣ Load a reference dataset
data = AmazonOffice(version='2014').prepare_and_load()

# 2️⃣ Apply preprocessing filters
data = FilterOutDuplicatedInteractions().run(data)
data = UserItemIterativeKCore(cores=5).run(data)

# 3️⃣ Split into train/validation/test
splitter = RandomHoldOut(test_ratio=0.2, val_ratio=0.1, seed=42)
splits = splitter.run(data)

train, val, test = splits['train'], splits['val'], splits['test']


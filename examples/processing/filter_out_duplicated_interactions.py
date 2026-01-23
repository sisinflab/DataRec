import pandas as pd
from datarec import DataRec, RawData
from datarec.processing.rating import FilterOutDuplicatedInteractions


data = pd.DataFrame({
    'user': [1, 1, 1, 2, 2, 3],
    'item': [10, 10, 20, 10, 10, 30],
    'rating': [3, 5, 4, 2, 1, 5],
    'timestamp': [100, 200, 150, 50, 60, 10]
})
datarec = DataRec(RawData(data, user='user', item='item', rating='rating', timestamp='timestamp'))

flt_first = FilterOutDuplicatedInteractions(keep='first')
print(flt_first.run(datarec, verbose=False))

flt_latest = FilterOutDuplicatedInteractions(keep='latest')
print(flt_latest.run(datarec, verbose=False))

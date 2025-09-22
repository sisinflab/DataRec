import pandas as pd
from datarec.io import read_tabular
from datarec.data.dataset import DataRec


data = {
    "user": ["u1", "u1", "u2", "u3"],
    "item": ["i1", "i2", "i2", "i3"],
    "rating": [5, 3, 4, 2],
    "timestamp": [1694300000, 1694300500, 1694310000, 1694320000],
}

df = pd.DataFrame(data)
df.to_csv("dummy.csv", index=False)


raw = read_tabular(
    filepath="dummy.csv",
    sep=",",
    user_col="user",
    item_col="item",
    rating_col="rating",
    timestamp_col="timestamp"
)

dummy_dr = DataRec(dataset_name='dummy', version_name='1')
dummy_dr.data = raw


print(dummy_dr)
print(f'{dummy_dr.dataset_name} has:\n'
      f'{dummy_dr.n_users} users\n'
      f'{dummy_dr.n_items} items\n'
      f'{dummy_dr.transactions} ratings\n')

print(f'{dummy_dr.dataset_name} metrics:')
for metric in dummy_dr.metrics:
    print(metric, dummy_dr.__getattribute__(metric))
from datarec.io.readers import read_json, read_tabular
from datarec.data.dataset import DataRec

test_data = 'data/test/data/data.dat'
test_json = 'data/test/json/data.json'

d1 = read_tabular(test_data, sep='::', user_col=0, header=None)
print(d1)
dr = DataRec(d1)
print(dr)
dr.data = d1
print(dr.n_users)



d2 = read_json(test_json, user_field='user_id', item_field='business_id')
print(d2)
dr = DataRec(d2)
print(dr)
print(dr.n_users)



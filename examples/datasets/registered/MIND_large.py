from datarec.datasets import MIND
from datarec import set_cache_dir

if __name__ == '__main__':
    dataset = MIND('large')
    dataset.prepare()
    dr = dataset.load(resource_name='train')
    print(dr)
    print(
        f'{dr.dataset_name} has:\n'
        f'{dr.n_users} users\n'
        f'{dr.n_items} items\n'
        f'{dr.transactions} ratings\n')
    dataset.prepare(resource_types='interactions', only_required=False)
    print(dataset.load(resource_name='validation'))
    print(dataset.load(resource_name='test'))

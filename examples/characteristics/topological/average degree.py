from datarec.datasets import Movielens

if __name__ == '__main__':
    
    dataset = Movielens(version='100k')
    dataset.prepare()
    dr = dataset.load()
    gr = dr.to_graphrec()
    print('average degree users' ,gr.characteristic('average_degree_users'))
    print('average degree items' ,gr.characteristic('average_degree_items'))
    print('average degree log' ,gr.characteristic('average_degree_log'))
    print('average degree users log' ,gr.characteristic('average_degree_users_log'))
    print('average degree items log' ,gr.characteristic('average_degree_items_log'))


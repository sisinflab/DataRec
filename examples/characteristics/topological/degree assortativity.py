from datarec.datasets import Movielens

if __name__ == '__main__':
    
    dataset = Movielens(version='100k')
    dataset.prepare()
    dr = dataset.load()
    gr = dr.to_graphrec()
    print('degree assortativity users' ,gr.characteristic('degree_assortativity_users'))
    print('degree assortativity items' ,gr.characteristic('degree_assortativity_items'))
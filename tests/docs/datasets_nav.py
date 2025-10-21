from docs.autobuild import datasets_nav

def test_retrieve_dataset_module():
    datasets_nav.retrieve_module_dataset_by_name(dataset_name='movielens')
    datasets_nav.retrieve_module_dataset_by_name(dataset_name='lastfm')
    datasets_nav.retrieve_module_dataset_by_name(dataset_name='epinions')
    datasets_nav.retrieve_module_dataset_by_name(dataset_name='ambar')

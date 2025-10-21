import importlib
from importlib import resources
import yaml
from datarec.io.paths import registry_dataset_filepath

def build_readme(dataset_name: str) -> None:
    """
    Build a readme file for the dataset indicated by dataset_name.
    The readme file is stored in the dataset package
    Args:
        dataset_name (str): the name of the dataset
    Returns:
        None
    """
    with open(registry_dataset_filepath(dataset_name), 'r') as conf_file:
        config = yaml.safe_load(conf_file)

    module_path = config['datarec_module']
    module = importlib.import_module(module_path)
    with resources.files(module).joinpath("README_template.md").open("r") as readme_file:
        readme = readme_file.read()
    readme = readme.replace('DATASET_NAME', config['dataset_name'])
    readme = readme.replace('DATASET_DESCRIPTION', config['description'])
    readme = readme.replace('URL', config['source'])
    readme = readme.replace('CITATION', config['citation'])
    readme = readme.replace('VERSION', "-\n\t".join(config['versions']))
    readme = readme.replace('LATEST_VERSION', str(config['latest_version']))
    readme_path = str(resources.files(module).joinpath("README.md"))
    with open(readme_path, 'w') as rff:
        rff.write(readme)
    print('Wrote README to: {}'.format(readme_path))


if __name__ == '__main__':
    build_readme('ambar')
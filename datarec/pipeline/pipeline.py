import yaml
import importlib
from datarec.pipeline.pipeline_step import PipelineStep
from typing import Dict, Any, List


class Pipeline:
    def __init__(self):
        self.steps: List[PipelineStep] = []

    def add_step(self, name: str, operation: str, params: Dict[str, Any]) -> None:
        if self.steps:
            last_step = self.steps[-1]
            if last_step.name == 'split':
                if name != 'export':
                    raise ValueError(f"Error: After a 'split' step, "
                                     f"the next step *must* be an 'export'. "
                                     f"You attempted to add a '{name}' step.")

        self.steps.append(PipelineStep(name, operation, params))

    def to_yaml(self, file_path: str) -> None:
        with open(file_path, "w") as f:
            yaml.dump({"pipeline": [step.to_dict() for step in self.steps]}, f)

    def copy(self):
        pipeline = Pipeline()
        pipeline.steps = [step.copy() for step in self.steps]
        return pipeline

    @classmethod
    def from_yaml(cls, file_path: str):
        with open(file_path, "r") as f:
            config = yaml.safe_load(f)

        pipeline = cls()
        for step in config.get("pipeline", []):
            pipeline.add_step(step['name'], step["operation"], step["params"])

        return pipeline

    @staticmethod
    def get_transformation_class(package_name: str, class_name: str):
        mapping = {
            'load': 'datasets',
            'process': 'processing',
            'split': 'splitters',
            'export': 'io'
        }

        if package_name not in mapping.keys():
            raise ValueError(f"Unknown package name '{package_name}'")

        module_name = "datarec." + mapping[package_name]

        if package_name == 'export':
            module = importlib.import_module(module_name)
            return getattr(module, "FrameworkExporter")

        try:
            module = importlib.import_module(module_name)
            return getattr(module, class_name)
        except (ModuleNotFoundError, AttributeError) as e:
            raise ImportError(f"Could not find class {class_name} in module {module_name}") from e

    def apply(self):
        frameworks = {
            'Elliot': 'to_elliot',
            'ClayRS': 'to_clayrs',
            'Cornac': 'to_cornac',
            'DaisyRec': 'to_daisyrec',
            'LensKit': 'to_lenskit',
            'RecBole': 'to_recbole',
            'ReChorus': 'to_rechorus',
            'RecPack': 'to_recpack',
            'Recommenders': 'to_recommenders'
        }

        if self.steps[0].name != 'load':
            raise ValueError(f'The first pipeline step must be a load, not {self.steps[0].name}')

        print(f"\n\n --- Reproducing Pipeline --- \n\n")

        for step in self.steps:
            func = self.get_transformation_class(step.name, step.operation)
            if not func:
                raise ValueError(f"Unknown operation: {step.operation}")

            if step.name == 'load':
                print(f"Pipeline step {step.name}.")
                print(f"Loading dataset: {func}.")
                result = func(**step.params).prepare_and_load()

            elif step.name == 'export':
                print(f"Pipeline step {step.name}.")
                print(f"Exporting dataset for {step.operation}.")
                function_name = frameworks[step.operation]
                exporter = func(**step.params)
                getattr(exporter, function_name)(result['train'],
                                                 result['test'],
                                                 result['val'])
                return
            else:
                print(f"Pipeline step {step.name}.")
                print(f"Applying {func}.")
                result = func(**step.params).run(result)

        print(f"\n\n --- Finished Pipeline --- \n\n")
        return result
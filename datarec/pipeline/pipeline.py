import yaml
import importlib
from pathlib import Path
from typing import Dict, Any, List, Optional, TYPE_CHECKING

from datarec.pipeline.pipeline_step import PipelineStep
from datarec.io.rawdata import RawData

# Pipeline usage overview:
# - Step keywords: load, read, process, split, export, write.
# - load: only for registry datasets (operation: registry_dataset).
# - read: file-based readers from datarec.io.readers (operation: read_*).
# - process: transformations from datarec.processing (operation: class name).
# - split: splitters from datarec.splitters (operation: class name).
# - export: framework exporters (operation: Elliot, RecBole, etc.).
# - write: writers from datarec.io.writers (operation: write_*).
# - input_folder is used by read steps with filename; output_folder by export/write steps.
# - For read/write, use filename in params and pass base folders to apply().
# - Some exporters (e.g., Elliot, ReChorus) require split results.

if TYPE_CHECKING:
    from datarec.data.dataset import DataRec


class Pipeline:
    """Pipeline for reproducible data transformations."""
    def __init__(self):
        self.steps: List[PipelineStep] = []

    def __str__(self) -> str:
        """Return a readable summary of pipeline steps."""
        if not self.steps:
            return "Pipeline(steps=0)"
        lines = ["Pipeline:"]
        for idx, step in enumerate(self.steps, start=1):
            params = ", ".join(f"{k}={v!r}" for k, v in step.params.items())
            lines.append(f"{idx}. {step.name} -> {step.operation}({params})")
        return "\n".join(lines)

    def add_step(self, name: str, operation: str, params: Dict[str, Any]) -> None:
        """Add a pipeline step.

        Args:
            name (str): Step name (load/read/process/split/export/write).
            operation (str): Operation or class name for the step.
            params (Dict[str, Any]): Parameters for the step.
        """
        self.steps.append(PipelineStep(name, operation, params))

    def to_yaml(self, file_path: str) -> None:
        """Serialize pipeline to YAML.

        Args:
            file_path (str): Path to the output YAML file.
        """
        with open(file_path, "w") as f:
            yaml.dump({"pipeline": [step.to_dict() for step in self.steps]}, f)

    @classmethod
    def from_yaml(cls, file_path: str) -> "Pipeline":
        """Load a pipeline from YAML.

        Args:
            file_path (str): Path to a YAML pipeline file.

        Returns:
            Pipeline: The loaded pipeline instance.
        """
        with open(file_path, "r") as f:
            config = yaml.safe_load(f)

        pipeline = cls()
        for step in config.get("pipeline", []):
            pipeline.add_step(step['name'], step["operation"], step["params"])

        return pipeline

    def copy(self) -> "Pipeline":
        """Deep-copy the pipeline steps.

        Returns:
            Pipeline: A copy of this pipeline with duplicated steps.
        """
        pipeline = Pipeline()
        pipeline.steps = [step.copy() for step in self.steps]
        return pipeline

    def apply(self, input_folder: Optional[str] = None, output_folder: Optional[str] = None) -> Any:
        """Execute the pipeline.

        Args:
            input_folder (Optional[str]): Base folder for file-based read steps.
            output_folder (Optional[str]): Base folder for export/write steps.

        Returns:
            Any: The final DataRec or split dict, depending on pipeline steps.
        """
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
        split_required = {'Elliot', 'ReChorus'}

        if not self.steps:
            raise ValueError("Pipeline is empty. Add at least a load step.")
        if self.steps[0].name not in {'load', 'read'}:
            raise ValueError(f"The first pipeline step must be a load or read, not {self.steps[0].name}")

        print(f"\n\n --- Reproducing Pipeline --- \n\n")

        for step in self.steps:
            print(f"\n--- Step: {step.name} -> {step.operation} ---\n")
            func = self.get_transformation_class(step.name, step.operation)
            if not func:
                raise ValueError(f"Unknown operation: {step.operation}")

            if step.name == 'load':
                result = self._apply_load(step, func, input_folder)

            elif step.name == 'read':
                result = self._apply_read(step, func, input_folder)

            elif step.name == 'export':
                if step.operation not in frameworks:
                    raise ValueError(f"Export step requires a framework operation. Unknown: {step.operation}")
                self._apply_export(step, func, result, output_folder, frameworks, split_required)
                return

            elif step.name == 'write':
                self._apply_write(step, func, result, output_folder)
                return
            else:
                result = self._apply_transform(step, func, result)

        print(f"\n\n --- Finished Pipeline --- \n\n")
        return result

    def _apply_load(self, step: PipelineStep, func, input_folder: Optional[str]) -> Any:
        print(f"Pipeline step {step.name}.")
        print(f"Loading dataset via: {step.operation}.")
        params = dict(step.params)
        if step.operation == "registry_dataset":
            loaded = func(**params)
        else:
            raise ValueError("Load step supports only 'registry_dataset'. Use 'read' for file-based inputs.")
        if hasattr(loaded, "prepare_and_load"):
            return loaded.prepare_and_load()
        if hasattr(loaded, "data"):
            return loaded
        raise ValueError(f"Loader '{step.operation}' did not return a DataRec or an object with prepare_and_load.")

    def _apply_read(self, step: PipelineStep, func, input_folder: Optional[str]) -> Any:
        print(f"Pipeline step {step.name}.")
        print(f"Reading dataset via: {step.operation}.")
        params = dict(step.params)
        if input_folder is None:
            raise ValueError("Read step requires input_folder and 'filename' in params.")
        if "filepath" in params:
            raise ValueError("Read step does not accept 'filepath' in pipelines. Use 'filename' and pass input_folder to apply().")
        filename = params.pop("filename", None)
        if not filename:
            raise ValueError("Read step requires 'filename' in params.")
        params["filepath"] = str(Path(input_folder) / filename)
        loaded = func(**params)
        if hasattr(loaded, "data"):
            return loaded
        raise ValueError(f"Reader '{step.operation}' did not return a DataRec/RawData.")

    def _apply_transform(self, step: PipelineStep, func, result):
        print(f"Pipeline step {step.name}.")
        print(f"Applying {func}.")
        return func(**step.params).run(result)

    def _apply_export(
        self,
        step: PipelineStep,
        func,
        result,
        output_folder: Optional[str],
        frameworks: Dict[str, str],
        split_required: set,
    ) -> None:
        print(f"Pipeline step {step.name}.")
        print(f"Exporting dataset for {step.operation}.")
        params = dict(step.params)
        if output_folder is None:
            if "filename" in params and "output_path" in params:
                raise ValueError("Framework export should not include both 'filename' and 'output_path'.")
            if "filename" in params and "output_path" not in params:
                raise ValueError("Framework export requires output_folder when using 'filename' in params.")
            if "output_path" not in params:
                raise ValueError("Framework export requires 'output_path' or 'filename' in params.")
        else:
            if "output_path" in params:
                raise ValueError("Framework export does not accept 'output_path' when output_folder is provided. Use 'filename'.")
            filename = params.pop("filename", None)
            if not filename:
                raise ValueError("Framework export requires 'filename' in params.")
            params["output_path"] = str(Path(output_folder) / filename)
        exporter = func(**params)
        function_name = frameworks[step.operation]
        if isinstance(result, dict):
            if step.operation in split_required:
                train = result.get('train')
                test = result.get('test')
                val = result.get('val')
                if train is None or test is None:
                    raise ValueError(f"Export '{step.operation}' requires train/test splits.")
                getattr(exporter, function_name)(train, test, val)
            else:
                export_data = result.get('train')
                if export_data is None and len(result) == 1:
                    export_data = next(iter(result.values()))
                if export_data is None:
                    raise ValueError(f"Export '{step.operation}' does not support split dicts without a train split.")
                getattr(exporter, function_name)(export_data)
        else:
            if step.operation in split_required:
                raise ValueError(f"Export '{step.operation}' requires a split result (train/test[/val]).")
            getattr(exporter, function_name)(result)
        return

    def _apply_write(
        self,
        step: PipelineStep,
        func,
        result,
        output_folder: Optional[str],
    ) -> None:
        print(f"Pipeline step {step.name}.")
        print(f"Writing dataset via: {step.operation}.")
        params = dict(step.params)
        if output_folder is None:
            if "filename" in params and "filepath" not in params:
                raise ValueError("Write step requires output_folder when using 'filename' in params.")
            if "filename" in params and "filepath" in params:
                raise ValueError("Write step should not include both 'filename' and 'filepath'.")
            if "filepath" not in params:
                raise ValueError("Write step requires 'filepath' or 'filename' in params.")
            base_path = Path(params.get("filepath"))
        else:
            if "filepath" in params:
                raise ValueError("Write step does not accept 'filepath' when output_folder is provided. Use 'filename'.")
            filename = params.pop("filename", None)
            if not filename:
                raise ValueError("Write step requires 'filename' in params.")
            base_path = Path(output_folder) / filename
        if isinstance(result, dict):
            split_param = params.pop("split", None)
            if split_param:
                split_data = result.get(split_param)
                if split_data is None:
                    raise ValueError(f"Split '{split_param}' not found for writer export.")
                params["filepath"] = str(base_path)
                func(split_data, **params)
            else:
                for split_name, split_data in result.items():
                    split_path = _with_split_suffix(base_path, split_name)
                    params["filepath"] = str(split_path)
                    func(split_data, **params)
        else:
            params["filepath"] = str(base_path)
            func(result, **params)

    @staticmethod
    def get_transformation_class(package_name: str, class_name: str) -> Any:
        """Resolve a pipeline step to its callable class/function.

        Args:
            package_name (str): Pipeline step name (load/process/split/export).
            class_name (str): Class name or special loader name.

        Returns:
            Any: Callable class/function implementing the step.
        """
        mapping = {
            'load': 'datasets',
            'process': 'processing',
            'split': 'splitters',
            'export': 'io',
            'read': 'io',
            'write': 'io',
        }

        if package_name not in mapping.keys():
            raise ValueError(f"Unknown package name '{package_name}'")

        module_name = "datarec." + mapping[package_name]

        if package_name == 'load':
            if class_name == "registry_dataset":
                return _load_registry_dataset
            readers_module = importlib.import_module("datarec.io.readers")
            if hasattr(readers_module, class_name):
                return getattr(readers_module, class_name)
            raise ImportError(
                f"Could not find reader '{class_name}' in datarec.io.readers."
            )
        if package_name == 'read':
            readers_module = importlib.import_module("datarec.io.readers")
            if hasattr(readers_module, class_name):
                return getattr(readers_module, class_name)
            raise ImportError(
                f"Could not find reader '{class_name}' in datarec.io.readers."
            )
        if package_name == 'export':
            module = importlib.import_module(module_name)
            return getattr(module, "FrameworkExporter")
        if package_name == 'write':
            writers_module = importlib.import_module("datarec.io.writers")
            if hasattr(writers_module, class_name):
                return getattr(writers_module, class_name)
            raise ImportError(
                f"Could not find writer '{class_name}' in datarec.io.writers."
            )
        try:
            module = importlib.import_module(module_name)
            return getattr(module, class_name)
        except (ModuleNotFoundError, AttributeError) as e:
            raise ImportError(f"Could not find class {class_name} in module {module_name}") from e


# --- Loader helpers ----------------------------------------------------------

def _load_registry_dataset(dataset_name: str, version: str = "latest", **kwargs):
    """
    Loader for datasets declared in the registry (Dataset builder).

    Args:
        dataset_name (str): Registered dataset name.
        version (str): Dataset version or "latest".
        **kwargs: Extra dataset constructor arguments.

    Returns:
        Dataset: A dataset builder instance.
    """
    from datarec.data.datarec_builder import RegisteredDataset
    return RegisteredDataset(dataset_name=dataset_name, version=version, **kwargs)


def _with_split_suffix(path: Path, split_name: str) -> Path:
    """
    Insert the split name before the file suffix.

    Args:
        path (Path): Base output path.
        split_name (str): Split key (e.g., train/test/val).

    Returns:
        Path: Path with split suffix injected.
    """
    if path.suffix:
        return path.with_name(f"{path.stem}_{split_name}{path.suffix}")
    return path.with_name(f"{path.name}_{split_name}")

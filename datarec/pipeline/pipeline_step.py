from typing import Dict, Any


class PipelineStep:
    def __init__(self, name: str, operation: str, params: Dict[str, Any]):

        self.name = name
        self.operation = operation
        self.params = params

    def copy(self):
        return PipelineStep(self.name, self.operation, self.params)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "operation": self.operation, "params": self.params}

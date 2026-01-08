from typing import Dict, Any


class PipelineStep:
    def __init__(self, name: str, operation: str, params: Dict[str, Any]):

        self.name = name
        self.operation = operation
        self.params = params

    def __str__(self) -> str:
        params = ", ".join(f"{k}={v!r}" for k, v in self.params.items())
        return f"{self.name} -> {self.operation}({params})"

    def copy(self):
        return PipelineStep(self.name, self.operation, self.params)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "operation": self.operation, "params": self.params}

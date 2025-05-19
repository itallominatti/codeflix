from dataclasses import dataclass

@dataclass
class Notification:
    def __init__(self) -> None:
        self._errors: list[dict] = []

    def add_error(self, field: str, message: str) -> None:
        self._errors.append({"field": field, "message": message})

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def get_errors(self) -> list[dict]:
        return self._errors

    @property
    def messages(self) -> str:
        return ",".join([f"{error['field']}: {error['message']}" for error in self._errors])
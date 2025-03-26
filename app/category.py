import uuid
from uuid import UUID

class Category:
    def __init__(
        self,
        name: str,
        id: UUID = "",
        description: str = "",
        is_active: bool = True
    ) -> None:
        self.id = id or uuid.uuid4()
        self.name = name
        self.description = description
        self.is_active = is_active

        self.validate()

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name must have less 256 characters")

        if len(self.name) == 0:
            raise ValueError("name cannot be empty")

    def __str__(self):
        return f"{self.name} - {self.description} ({self.is_active})"

    def __repr__(self):
        return f"<Category {self.name} ({self.id})>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def update_category(self, name: str, description: str):
        self.name = name
        self.description = description

        self.validate()

    def activate(self) -> None:
        self.is_active = True

        self.validate()

    def deactivate(self) -> None:
        self.is_active = False

        self.validate()
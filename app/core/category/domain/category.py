from dataclasses import dataclass, field
from app.core._shared.entity import Entity

@dataclass
class Category(Entity):
    name: str
    description: str = ""
    is_active: bool = True

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            self.notification.add_error("name", "name must have less 256 characters")

        if len(self.name) == 0:
            self.notification.add_error("name", "name cannot be empty")

        if len(self.description) > 1024:
            self.notification.add_error("description", "description cannot be longer than 1024")

        if self.notification.has_errors():
            raise ValueError(self.notification.messages)

    def __str__(self):
        return f"{self.name} - {self.description} ({self.is_active})"

    def __repr__(self):
        return f"<Category {self.name} ({self.id})>"

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
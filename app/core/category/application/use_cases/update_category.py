from dataclasses import dataclass
from uuid import UUID
from app.core.category.domain.category_repository import CategoryRepository
from app.core.category.application.exceptions import CategoryNotFound


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str or None = None
    description: str or None = None
    is_active: bool or None = None

class UpdateCategory:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    def execute(self, request: UpdateCategoryRequest) -> None:
        category = self.repository.get_by_id(request.id)
        if not category:
            raise CategoryNotFound(f"Category {request.id} not found")

        current_name = category.name
        current_description = category.description

        if request.name is not None:
            current_name = request.name

        if request.description is not None:
            current_description = request.description

        if request.is_active is True:
            category.activate()

        if request.is_active is False:
            category.deactivate()

        category.update_category(name=current_name, description=current_description)
        self.repository.update(category)

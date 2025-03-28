from uuid import UUID
from dataclasses import dataclass

from app.core.category.domain.category import Category

from app.core.category.application.exceptions import InvalidCategoryData, CategoryNotFound
from app.core.category.application.category_repository import CategoryRepository

@dataclass
class DeleteCategoryRequest:
    id: UUID


class DeleteCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self,request: DeleteCategoryRequest) -> None:
        category = self.repository.get_by_id(id=request.id)

        if category is None:
            raise CategoryNotFound(f"Category with {request.id} not found")

        self.repository.delete(category.id)



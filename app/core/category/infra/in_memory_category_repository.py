from uuid import UUID
from typing import Optional

from app.core.category.application.category_repository import CategoryRepository
from app.core.category.domain.category import Category

class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories=None) -> None:
        self.categories = categories or []

    def save(self, category: Category) -> None:
        self.categories.append(category)

    def get_by_id(self, id: UUID) -> Optional[Category]:
        for category in self.categories:
            if category.id == id:
                return category
        return None
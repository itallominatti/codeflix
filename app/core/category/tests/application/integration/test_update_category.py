import uuid

import pytest

from app.core.category.domain.category import Category
from app.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from app.core.category.application.use_cases.update_category import UpdateCategory,UpdateCategoryRequest
from app.core.category.application.exceptions import CategoryNotFound


class TestUpdateCategory:
    def test_can_update_category_name_and_description(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Série",
            description="Categoria para séries"
        )
        use_case.execute(request)

        updated_category = repository.get_by_id(category.id)
        assert category.name == "Série"
        assert category.description == "Categoria para séries"

    def test_try_updated_category_when_does_not_exist_then_raise_exception(self):
        category_movie = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True
        )
        category_serie = Category(
            name='Série',
            description="Categoria para séries",
            is_active=True
        )
        repository = InMemoryCategoryRepository(
            categories=[category_movie, category_serie]
        )
        use_case = UpdateCategory(
            repository=repository
        )
        request = UpdateCategoryRequest(
            id="aaaaa",
            name="Série"
        )

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)
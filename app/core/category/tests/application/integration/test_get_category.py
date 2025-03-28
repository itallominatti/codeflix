import uuid
from uuid import UUID

import pytest

from app.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from app.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from app.core.category.domain.category import Category
from app.core.category.application.exceptions import CategoryNotFound

class TestGetCategory:
    def test_get_category_by_id(self):
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
        use_case = GetCategory(
            repository=repository
        )
        request = GetCategoryRequest(
            id=category_movie.id
        )
        response = use_case.execute(request)
        assert response == GetCategoryResponse(
            id=category_movie.id,
            description=category_movie.description,
            name=category_movie.name,
            is_active=True
        )

    def test_when_category_does_not_exist_thein_raise_exception(self):
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
        use_case = GetCategory(
            repository=repository
        )
        request = GetCategoryRequest(
            id=uuid.uuid4()
        )

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)

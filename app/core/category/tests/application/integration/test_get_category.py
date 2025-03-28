import uuid
from uuid import UUID

import pytest

from app.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from app.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from app.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from app.core.category.domain.category import Category
from app.core.category.application.exceptions import CategoryNotFound

class TestDeleteCategory:
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
        use_case = DeleteCategory(
            repository=repository
        )
        request = DeleteCategoryRequest(
            id=category_movie.id
        )
        assert repository.get_by_id(category_movie.id) is not None
        response = use_case.execute(request)


        assert repository.get_by_id(category_movie.id) is None
        assert response is None

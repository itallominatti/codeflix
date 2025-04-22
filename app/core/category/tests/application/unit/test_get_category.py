import uuid
from unittest.mock import create_autospec

import pytest

from app.core.category.application.exceptions import CategoryNotFound
from app.core.category.application.use_cases.get_category import GetCategoryRequest, GetCategoryResponse, GetCategory
from app.core.category.domain.category_repository import CategoryRepository
from app.core.category.domain.category import Category


class TestGetCategory:
    def test_return_found_category(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(
            id=category.id
        )
        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category.id,
            name="Filme",
            description="Categoria para filmes",
            is_active=True
        )

    def test_when_category_not_found_then_raise_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=uuid.uuid4())

        with pytest.raises(CategoryNotFound):
            use_case.execute(request)
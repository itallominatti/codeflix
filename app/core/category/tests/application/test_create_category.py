from uuid import UUID

import pytest

from app.core.category.application.create_category import create_category
from app.core.category.application.create_category import InvalidCategoryData

class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        category_id = create_category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True)

        assert category_id is not None
        assert isinstance(category_id, UUID)

    def test_create_category_with_invalid_data(self):
        with pytest.raises(InvalidCategoryData, match="name cannot be empty") as exc_info:
            category_id = create_category(
                name=""
            )

            assert exc_info.type is InvalidCategoryData
            assert str(exc_info.value) == "name cannot be empty"
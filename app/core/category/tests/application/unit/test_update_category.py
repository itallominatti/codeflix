from unittest.mock import create_autospec
import uuid
from app.core.category.application.category_repository import CategoryRepository
from app.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from app.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(
            id=uuid.uuid4(),
            name="Filme",
            description="Categoria para filmes",
            is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            name="Série",
            id=category.id
        )
        response = use_case.execute(request)

        assert category.name == "Série"
        assert category.description == "Categoria para filmes"
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(self):
        pass

    def test_can_deactivate_category(self):
        pass

    def test_can_activate_category(self):
        pass
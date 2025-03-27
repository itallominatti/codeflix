from uuid import UUID

from app.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from app.core.category.application.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse

class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(
            repository=repository
        )
        request = CreateCategoryRequest(
            name="Filme",
            description="Categoria para filmes"
        )
        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response,CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1

        persisted_category = repository.categories[0]

        assert persisted_category.id == response.id
        assert persisted_category.name == "Filme"
        assert persisted_category.description == "Categoria para filmes"
        assert persisted_category.is_active == True
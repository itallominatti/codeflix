from app.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from app.core.category.domain.category import Category

class TestInMemoryCategoryRepository:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name="Filme",
            description="Categoria para filmes",
        )

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

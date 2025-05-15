import uuid
from unittest.mock import create_autospec

import pytest

from app.core.category.domain.category_repository import CategoryRepository
from app.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from app.core.genre.application.exceptions import RelatedCategoriesNotFound

from app.core.genre.application.use_cases.create_genre import CreateGenre

from app.core.category.domain.category import Category
from app.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def category_repository(movie_category, documentary_category) -> CategoryRepository:
    return InMemoryCategoryRepository(
        categories=[movie_category, documentary_category]
    )

class TestCreateGenre:
    def test_create_genre_with_associated_categories(
        self,
        movie_category,
        documentary_category,
        category_repository
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        input = CreateGenre.Input(
            name="Action",
            categories={movie_category.id, documentary_category.id}
        )

        output = use_case.execute(input)

        assert isinstance(output.id, uuid.UUID)
        saved_genre = genre_repository.get_by_id(output.id)

        assert saved_genre is not None

    def test_create_genre_with_inexistent_categories_raise_an_error(
        self,
        category_repository
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        input = CreateGenre.Input(
            name="Action",
            categories={uuid.uuid4()}
        )

        with pytest.raises(
            expected_exception=RelatedCategoriesNotFound,
        ):
            output = use_case.execute(input)


    def test_create_genre_without_categories(
        self,
            category_repository
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        input = CreateGenre.Input(
            name="Action",
        )

        output = use_case.execute(input)
        genre_saved = genre_repository.get_by_id(output.id)

        assert output.id is not None
        assert genre_saved.categories == set({})
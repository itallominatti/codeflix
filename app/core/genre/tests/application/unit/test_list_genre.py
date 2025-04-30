import uuid
from unittest.mock import create_autospec

import pytest

from app.core.category.domain.category_repository import CategoryRepository
from app.core.genre.application.exceptions import RelatedCategoriesNotFound, InvalidGenre
from app.core.genre.application.use_cases.list_genre import ListGenre
from app.core.genre.domain.genre_repository import GenreRepository

from app.core.genre.domain.genre import Genre
from app.core.category.domain.category import Category

@pytest.fixture
def romance_genre() -> Genre:
    return Genre(
        name="Romance"
    )

@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def mock_category_repository_with_categories(
    movie_category: Category,
    documentary_category: Category
) -> Category:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository

@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository

class TestListGenre:
    def test_when_categories_is_empty(self, mock_genre_repository):
        use_case = ListGenre(repository=mock_genre_repository)
        input = ListGenre.Input()
        output = use_case.execute(input)

        assert output == ListGenre.Output(data=[])

    def test_return_a_valid_genre(self, mock_genre_repository, romance_genre):
        use_case = ListGenre(repository=mock_genre_repository)
        input = ListGenre.Input()
        mock_genre_repository.list.return_value = [romance_genre]

        output = use_case.execute(input)

        assert len(output.data) == 1
        assert output.data[0].id == romance_genre.id
        assert output.data[0].name == romance_genre.name


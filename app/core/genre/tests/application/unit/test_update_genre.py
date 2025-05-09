import uuid
from unittest.mock import create_autospec

import pytest

from app.core.genre.application.exceptions import GenreNotFound, RelatedCategoriesNotFound
from app.core.genre.application.use_cases.create_genre import CreateGenre
from app.core.genre.application.use_cases.update_genre import UpdateGenre
from app.core.genre.domain.genre import Genre
from app.core.genre.domain.genre_repository import GenreRepository
from app.core.category.domain.category_repository import CategoryRepository


@pytest.fixture
def mock_genre_repository():
    return create_autospec(GenreRepository)

@pytest.fixture
def mock_category_repository():
    return create_autospec(CategoryRepository)

class TestUpdateGenre:
    def test_update_genre_name(
        self,
        mock_genre_repository,
        mock_category_repository,
    ):
        genre = Genre(name="Romance")
        mock_genre_repository.get_by_id.return_value = genre


        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository,
        )
        input = UpdateGenre.Input(
            name='Drama',
            is_active=genre.is_active,
            categories=genre.categories,
            id=genre.id
        )
        use_case.execute(input)
        assert input.name == genre.name

    def test_update_genre_activate(
        self,
        mock_genre_repository,
        mock_category_repository,
    ):
        genre = Genre(name="Romance", is_active=False)
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository,
        )
        input = UpdateGenre.Input(
            name=genre.name,
            categories=genre.categories,
            is_active=True,
            id=genre.id
        )
        use_case.execute(input)
        assert genre.is_active == True

    def test_update_genre_deactivate(
        self,
        mock_genre_repository,
        mock_category_repository,
    ):
        genre = Genre(name="Romance", is_active=True)
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository,
        )
        input = UpdateGenre.Input(
            name=genre.name,
            categories=genre.categories,
            is_active=False,
            id=genre.id
        )
        use_case.execute(input)
        assert genre.is_active == False

    def test_update_categories_when_categories_not_found(
            self,
            mock_genre_repository,
            mock_category_repository
    ):
        genre = Genre(name="Romance", is_active=True, categories={uuid.uuid4(), uuid.uuid4()})
        mock_genre_repository.get_by_id.return_value = genre

        missing_categories = {uuid.uuid4(), uuid.uuid4()}
        mock_category_repository.get_by_id.side_effect = lambda cat_id: None

        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository,
        )
        input = UpdateGenre.Input(
            name=genre.name,
            categories=missing_categories,
            is_active=False,
            id=genre.id
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)

    def test_update_genre_when_genre_not_found(
        self,
        mock_genre_repository,
        mock_category_repository
    ):
        genre = Genre(name="Romance", is_active=True, categories={uuid.uuid4(), uuid.uuid4()})
        mock_genre_repository.get_by_id.return_value = None

        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository,
        )
        input = UpdateGenre.Input(
            name=genre.name,
            categories=genre.categories,
            is_active=False,
            id=uuid.uuid4()
        )

        with pytest.raises(GenreNotFound):
            use_case.execute(input)



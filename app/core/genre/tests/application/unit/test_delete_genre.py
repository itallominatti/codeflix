import uuid
from unittest.mock import create_autospec

import pytest

from app.core.genre.application.exceptions import GenreNotFound
from app.core.genre.application.use_cases.delete_genre import DeleteGenre
from app.core.genre.domain.genre import Genre
from app.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository():
    return create_autospec(GenreRepository)

class TestDeleteGenre:
    def test_when_genre_does_not_exist_then_raise_not_found(
        self,
        mock_genre_repository
    ):
        genre = Genre(name="Romance")
        mock_genre_repository.get_by_id.return_value = genre

        use_case = DeleteGenre(repository=mock_genre_repository)
        use_case.execute(input=DeleteGenre.Input(id=genre.id))

        mock_genre_repository.delete.assert_called_once_with(genre.id)

    def test_when_genre_from_repository(
        self,
        mock_genre_repository
    ):
        mock_genre_repository.get_by_id.return_value = None
        use_case = DeleteGenre(repository=mock_genre_repository)

        with pytest.raises(expected_exception=GenreNotFound, match="Genre with .* not found"):
            use_case.execute(input=DeleteGenre.Input(id=uuid.uuid4()))

        mock_genre_repository.delete.assert_not_called()
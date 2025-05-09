import pytest

from app.core.genre.domain.genre import Genre
from app.django_project.genre_app.repository import DjangoOrmGenreRepository
from app.django_project.genre_app.models import Genre as GenreORM


@pytest.mark.django_db
class TestSave:
    def test_saves_genre_in_database(self):
        genre = Genre(name="Action")
        genre_repository = DjangoOrmGenreRepository()

        GenreORM.objects.count() == 0
        genre_repository.save(genre)

        assert GenreORM.objects.count() == 1
        genre_model = GenreORM.objects.first()
        assert genre_model.id == genre.id
        assert genre_model.name == "Action"
        assert genre_model.is_active is True
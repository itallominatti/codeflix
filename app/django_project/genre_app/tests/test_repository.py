import uuid

import pytest
from django.db import transaction

from app.core.genre.domain.genre import Genre
from app.django_project.category_app.repository import DjangoORMCategoryRepository
from app.core.category.domain.category import Category
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

    def test_saves_genre_with_categories(self):
        repository = DjangoOrmGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(
            name="Action"
        )
        category_repository.save(category)

        genre = Genre(name="Action")
        genre.add_category(category.id)

        assert GenreORM.objects.count() == 0
        repository.save(genre)
        assert GenreORM.objects.count() == 1

        genre_model = GenreORM.objects.get(id=genre.id)
        related_category = genre_model.categories.get()

        assert  related_category.id == category.id
        assert related_category.name == "Action"

@pytest.mark.django_db
class TestGetById:
    def test_get_by_id_when_the_genre_exists(self):
        genre_repository = DjangoOrmGenreRepository()
        category_repository = DjangoORMCategoryRepository()
        category = Category(
            name="Action"
        )
        category_repository.save(category)

        genre = Genre(name="Action")
        genre.add_category(category.id)
        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        genre_model = GenreORM.objects.get(id=genre.id)
        related_category = genre_model.categories.get()

        assert related_category.id == category.id
        assert related_category.name == "Action"

    def test_get_by_id_when_the_genre_not_found(self):
        genre_repository = DjangoOrmGenreRepository()

        genre = Genre(name="Action")
        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        with pytest.raises(
                expected_exception=GenreORM.DoesNotExist,
                match="Genre matching query does not exist."
        ):
            genre_model = GenreORM.objects.get(id=uuid.uuid4())

@pytest.mark.django_db
class TestDelete:
    def test_delete_genre(self):
        genre_repository = DjangoOrmGenreRepository()

        genre = Genre(name="Action")
        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        GenreORM.objects.filter(id=genre.id).delete()

        assert GenreORM.objects.count() == 0

@pytest.mark.django_db
class TestUpdate:
    def test_try_update_genre_when_the_genre_doest_not_exist(self):
        genre_repository = DjangoOrmGenreRepository()

        genre = Genre(name="Action")
        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        with pytest.raises(
                expected_exception=GenreORM.DoesNotExist,
                match="Genre matching query does not exist."
        ):
            genre_model = GenreORM.objects.get(id=uuid.uuid4())

    def test_update_genre_name(self):
        genre_repository = DjangoOrmGenreRepository()

        genre = Genre(name="Action")
        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        with transaction.atomic():
            GenreORM.objects.filter(id=genre.id).update(
                name='Drama',
            )
        genre_updated = GenreORM.objects.get(id=genre.id)
        assert genre_updated.name == 'Drama'

    def test_activate_genre(self):
        genre_repository = DjangoOrmGenreRepository()

        genre = Genre(
            name="Action",
            is_active=False
        )
        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        old_genre = GenreORM.objects.get(id=genre.id)
        assert old_genre.is_active == False

        with transaction.atomic():
            GenreORM.objects.filter(id=genre.id).update(
                is_active=True
            )
        genre_updated = GenreORM.objects.get(id=genre.id)
        assert genre_updated.is_active == True

    def test_deactivate_genre(self):
        genre_repository = DjangoOrmGenreRepository()

        genre = Genre(
            name="Action",
            is_active=True
        )
        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        old_genre = GenreORM.objects.get(id=genre.id)
        assert old_genre.is_active == True

        with transaction.atomic():
            GenreORM.objects.filter(id=genre.id).update(
                is_active=False
            )
        genre_updated = GenreORM.objects.get(id=genre.id)
        assert genre_updated.is_active == False


    def test_update_genre_categories(self):
        genre_repository = DjangoOrmGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(
            name="Action"
        )
        category_repository.save(category)

        genre = Genre(
            name="Action",
            is_active=True
        )
        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        with transaction.atomic():
            genre_model = GenreORM.objects.get(id=genre.id)
            genre_model.categories.set({category.id})

















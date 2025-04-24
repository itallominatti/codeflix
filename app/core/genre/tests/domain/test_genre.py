import uuid
from uuid import UUID

import pytest

from app.core.genre.domain.genre import Genre

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Genre()

    def test_name_must_have_less_than_256_characters(self):
        with pytest.raises(ValueError, match="name must have less 256 characters"):
            Genre(name="a" * 256)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Genre(name="Drama")
        assert  isinstance(category.id, UUID)

    def test_created_genre_with_default_values(self):
        genre = Genre(name="Drama")
        assert genre.name == "Drama"
        assert genre.is_active is True
        assert isinstance(genre.id, UUID)
        assert genre.categories == set()

    def test_category_is_created_as_active_by_default(self):
        category = Genre("Filme")
        assert category.is_active is True

    def test_genre_is_created_with_provided_values(self):
        genre_id = uuid.uuid4()
        categories = {uuid.uuid4(), uuid.uuid4()}
        genre = Genre(
            id=genre_id,
            name="Drama",
            is_active=False,
            categories=categories
        )

        assert genre.id == genre_id
        assert genre.name == "Drama"
        assert genre.is_active is False
        assert genre.categories == categories

    def test_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Genre(name="")

class TestActivate:
    def test_activate_inactive_genre(self):
        genre = Genre(
            name="Drama",
            is_active=False
        )
        genre.activate()

        assert genre.is_active == True

    def test_activate_active_genre(self):
        genre = Genre(
            name="Filme",
            is_active=True
        )
        genre.activate()

        assert genre.is_active == True

class TestDeactivate:
    def test_deactivate_active_genre(self):
        genre = Genre(
            name="Filme"
        )
        genre.deactivate()

        assert genre.is_active == False

    def test_deactivate_inactive_category(self):
        genre = Genre(
            name="Filme",
            is_active=False
        )
        genre.deactivate()

        assert genre.is_active == False

class TestEquality:
    def test_when_genres_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()

        genre_1 = Genre(name="Drama", id=common_id)
        genre_2 = Genre(name="Drama", id=common_id)

        assert genre_1 == genre_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        genre = Genre(name="Drama", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert  genre != dummy

class TestChangeName:
    def test_change_name(self):
        genre = Genre(name="Romance")

        genre.change_name("Terror")

        assert genre.name == "Terror"

    def test_when_name_is_empty(self):
        genre = Genre("Romance")

        with pytest.raises(ValueError, match="name cannot be empty"):
            genre.change_name("")

class TestAddCategory:
    def test_add_category_to_genre(self):
        genre = Genre("Romance")
        category_id = uuid.uuid4()

        assert category_id not in genre.categories
        genre.add_category(category_id)
        assert category_id in genre.categories

class TestRemoveCategory:
    def test_remove_category_from_genre(self):
        category_id = uuid.uuid4()
        genre = Genre(name='Romance', categories={category_id})

        genre.remove_category(category_id)
        assert category_id not in genre.categories
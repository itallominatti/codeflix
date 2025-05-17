import uuid
from uuid import UUID

import pytest

from app.core.category.domain.category import Category

class TestCategory:

    def test_name_must_have_less_than_256_characters(self):
        with pytest.raises(ValueError, match="name must have less 256 characters"):
            Category(name="a" * 256)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category(name="Filme")
        assert  isinstance(category.id, UUID)

    def test_created_category_with_default_values(self):
        category = Category(name="Filme")
        assert category.name == "Filme"
        assert category.description == ""
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        category = Category("Filme")
        assert category.is_active is True

    def test_category_is_created_with_provided_values(self):
        cat_id = uuid.uuid4()
        category = Category(
            id=cat_id,
            name="Filme",
            description="generic film",
            is_active=False
        )

        assert category.id == cat_id
        assert category.name == "Filme"
        assert category.description == "generic film"
        assert category.is_active is False

    def test_category_str_method_return_category(self):
        category = Category(name="Filme", description="generic film")
        assert str(category) == f"{category.name} - {category.description} ({category.is_active})"

    def test_category_repr_method_return_category(self):
        category = Category(name="Filme", description="generic film")
        assert repr(category) == f"<Category {category.name} ({category.id})>"

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")

class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="Filme", description="Filmes em geral")

        category.update_category(name="Série", description="Séries em geral")

        assert category.name == "Série"
        assert category.description == "Séries em geral"

class TestActivate:
    def test_activate_inactive_category(self):
        category = Category(
            name="Filme",
            description="Filmes em geral",
            is_active=False
        )
        category.activate()

        assert category.is_active == True

    def test_activate_active_category(self):
        category = Category(
            name="Filme",
            description="Filmes em geral",
            is_active=True
        )
        category.activate()

        assert category.is_active == True

class TestDeactivate:
    def test_deactivate_active_category(self):
        category = Category(
            name="Filme", description="Filmes em geral"
        )
        category.deactivate()

        assert category.is_active == False

    def test_deactivate_inactive_category(self):
        category = Category(
            name="Filme",
            description="Filmes em geral",
            is_active=False
        )
        category.deactivate()

        assert category.is_active == False

class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()

        category_1 = Category(name="Filme", id=common_id)
        category_2 = Category(name="Filme", id=common_id)

        assert category_1 == category_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        category = Category(name="Filme", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert  category != dummy
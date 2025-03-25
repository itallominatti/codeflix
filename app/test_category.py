import unittest
import uuid
from uuid import UUID

import pytest

from category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

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
        assert category.is_active == True

    def test_category_is_created_as_active_by_default(self):
        category = Category("Filme")
        assert category.is_active == True

    def test_category_is_created_with_provided_values(self):
        cat_id = uuid.uuid4()
        category = Category(
            id=cat_id,
            name="Filme",
            description="generic film",
            is_active=False
        )
        self.assertEqual(category.id, cat_id)
        self.assertEqual(category.name, "Filme")
        self.assertEqual(category.description, "generic film")
        self.assertEqual(category.is_active, False)

    def test_category_str_method_return_category(self):
        category = Category(name="Filme", description="generic film")
        self.assertEqual(str(category), f"{category.name} - {category.description} ({category.is_active})")

    def test_category_repr_method_return_category(self):
        category = Category(name="Filme", description="generic film")
        self.assertEqual(repr(category), f"<Category {category.name} ({category.id})>")

if __name__ == "__main__":
    unittest.main()
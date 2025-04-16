import uuid
from uuid import UUID

import pytest

from app.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from app.core.category.application.use_cases.list_category import CategoryOutput,ListCategory,ListCategoryResponse
from app.core.category.domain.category import Category

class TestDeleteCategory:
    def test_return_empty_list(self):
        category_movie = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True
        )
        category_serie = Category(
            name='Série',
            description="Categoria para séries",
            is_active=True
        )
        repository = InMemoryCategoryRepository(
            categories=[]
        )
        use_case = ListCategory(
            repository=repository
        )
        response = use_case.execute()

        assert response == ListCategoryResponse(data=[])

    def test_return_existing_categories(self):
        def test_when_categories_in_repository_then_return_list(self):
            category_filme = Category(
                name="Filme",
                description="Categoria para filmes",
            )
            category_serie = Category(
                name="Serie",
                description="Categoria para series",
            )
            repository = InMemoryCategoryRepository
            repository.save(category_filme)
            repository.save(category_serie)

            use_case = ListCategory(repository=repository)
            response = use_case.execute()

            assert response == ListCategoryResponse(
                data=[
                    CategoryOutput(
                        id=category_serie.id,
                        name=category_serie.name,
                        description=category_serie.description,
                        is_active=category_serie.is_active
                    ),
                    CategoryOutput(
                        id=category_filme.id,
                        name=category_filme.name,
                        description=category_filme.description,
                        is_active=category_filme.is_active
                    )
                ]
            )

from uuid import UUID
from dataclasses import dataclass

from app.core.category.domain.category_repository import CategoryRepository
from app.core.genre.application.exceptions import GenreNotFound, RelatedCategoriesNotFound
from app.core.genre.domain.genre import Genre
from app.core.genre.domain.genre_repository import GenreRepository
from app.core.genre.tests.application.integration.test_create_genre import category_repository


class UpdateGenre:
    def __init__(
            self,
            repository: GenreRepository,
            category_repository: CategoryRepository
    ):
        self.repository = repository
        self.category_repository = category_repository
        self.categories_not_found = []

    @dataclass
    class Input:
        name: str or None
        is_active: bool or None
        categories: set[UUID] or None
        id: UUID



    def execute(self, input: Input) -> None:
        genre = self.repository.get_by_id(input.id)
        if not genre:
            raise GenreNotFound(
                f"Genre with {input.id} not found"
            )
        current_name = genre.name
        current_categories = genre.categories

        if input.name:
            current_name = input.name
            genre.change_name(name=current_name)

        if input.is_active is True:
            genre.activate()

        if input.is_active is False:
            genre.deactivate()

        if input.categories:
            current_categories = set()
            for category_id in input.categories:
                if not self.category_repository.get_by_id(category_id):
                    self.categories_not_found.append(category_id)
                else:
                    current_categories.add(category_id)

            if len(self.categories_not_found) >= 1:
                raise RelatedCategoriesNotFound(f"Categories not found: {self.categories_not_found}")

        genre_updated = Genre(
            name=current_name,
            is_active=genre.is_active,
            categories=current_categories,
            id=input.id
        )
        self.repository.update(genre_updated)









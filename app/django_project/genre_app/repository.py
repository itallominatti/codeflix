from typing import Optional
from uuid import UUID

from django.db import transaction

from app.core.genre.domain.genre import Genre
from app.core.genre.domain.genre_repository import GenreRepository
from app.django_project.genre_app.models import Genre as GenreORM



class DjangoOrmGenreRepository(GenreRepository):

    def save(self, genre: Genre):
        with transaction.atomic():
            genre_model = GenreORM.objects.create(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active
            )
            genre_model.categories.set(genre.categories)
            genre.categories


    def get_by_id(self, id: UUID) -> Optional[Genre]:
        ...


    def delete(self, id: UUID) -> None:
        ...


    def update(self, genre: Genre) -> None:
        ...

    def list(self) -> list[Genre]:
        ...
import uuid

import pytest


from rest_framework.test import APIClient

from app.core.genre.application.exceptions import GenreNotFound
from app.core.genre.domain.genre import Genre
from app.django_project.category_app.repository import DjangoORMCategoryRepository
from app.core.category.domain.category import Category
from app.django_project.genre_app.repository import DjangoOrmGenreRepository


@pytest.fixture
def category_movie() -> Category:
    return Category(
        name="Movie",
        description="Movie description"
    )
@pytest.fixture
def category_documentary() -> Category:
    return Category(
        name="Documentary",
        description="Documentary description"
    )

@pytest.fixture
def category_repository(category_documentary, category_movie) -> DjangoORMCategoryRepository:
    repo = DjangoORMCategoryRepository()
    repo.save(category_movie)
    repo.save(category_documentary)
    return repo

@pytest.fixture
def genre_romance() -> Genre:
    return Genre(
        name="Romance",
        is_active=True
    )

@pytest.fixture
def genre_drama() -> Genre:
    return Genre(
        name="Drama",
        is_active=True
    )

@pytest.fixture
def genre_repository(genre_romance, genre_drama) -> DjangoOrmGenreRepository:
    repo = DjangoOrmGenreRepository()
    repo.save(genre_romance)
    repo.save(genre_drama)
    return repo

@pytest.mark.django_db
class TestListAPI:
    @pytest.mark.skip(reason="Not implemented yet")
    def test_list_genres_and_categories(
            self,
            genre_repository,
            genre_romance,
            category_repository,
            category_movie,
            category_documentary,
            genre_drama
    ):
        url = "/api/genres/"
        response = APIClient().get(url)

        expected_response = {
            "data": [
                {
                    "id": str(genre_romance.id),
                    "name": "Romance",
                    "is_active": True,
                    "categories":  [
                        str(category_movie.id),
                        str(category_documentary.id)
                    ]
                },
                {
                    "id": str(genre_drama.id),
                    "name": "Drama",
                    "is_active": True,
                    "categories": []
                }
            ]
        }
        assert response.status_code == 200
        assert response.data == expected_response


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre_with_associated_categories(
            self,
            category_repository,
            genre_repository,
            genre_romance,
            category_movie,
    ):

        url = "/api/genres/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [
                str(category_movie.id)
            ]
        }
        response = APIClient().post(url, data=data)

        expected_response = {
            "id": str(genre_romance.id),
            "name": "Romance",
            "is_active": True,
            "categories": [
                str(category_movie.id)
            ]
        }
        assert response.status_code == 201
        assert response.data['id']
        created_genre_id = response.data["id"]

        genre_model = genre_repository.get_by_id(id=created_genre_id)
        assert genre_model is not None

@pytest.mark.django_db
class TestDeleteAPI:
    def test_delete_genre_when_the_genre_does_not_exist(
        self,
        genre_repository
    ):
        url = f"/api/genres/{uuid.uuid4()}/"
        response = APIClient().delete(url)
        assert response.status_code == 404
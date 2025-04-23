import uuid

import pytest

from rest_framework.test import APITestCase
from rest_framework import status

from app.core.category.domain.category import Category
from app.django_project.category_app.repository import DjangoORMCategoryRepository

@pytest.mark.django_db
class TestCategoryAPI(APITestCase):

    def test_when_id_is_invalid_return_400(self) -> None:
        url = '/api/categories/123123123123/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_list_categories(self):
        category_movie = Category(
            name="Movie",
            description="Movie Description",
        )
        category_documentary = Category(
            name="Documentary",
            description="Documentary Description",
        )

        repository = DjangoORMCategoryRepository()
        repository.save(category_movie)
        repository.save(category_documentary)

        url = "/api/categories/"
        response = self.client.get(url)

        expected_data = {
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active
                },
                {
                    "id": str(category_documentary.id),
                    "name": category_documentary.name,
                    "description": category_documentary.description,
                    "is_active": category_documentary.is_active
                },
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_return_category_when_exists(self) -> None:
        category_documentary = Category(
            name="Documentary",
            description="Documentary Description",
        )

        repository = DjangoORMCategoryRepository()
        repository.save(category_documentary)

        url = f"/api/categories/{category_documentary.id}/"
        response = self.client.get(url)
        expected_data = {
            "data": {
                "id": str(category_documentary.id),
                "name": "Documentary",
                "description": "Documentary Description",
                "is_active": True,
            }
        }
        assert response.data == expected_data
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_return_404_when_not_exists(self)-> None:
        id = uuid.uuid4()
        url = f'/api/categories/{id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_when_payload_is_invalid_then_return_400(self) -> None:
        url = f'/api/categories/'
        response = self.client.post(
            url,
            data={
                "name": '',
                "description": "Movie Description",
            })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."]
        }

    def test_when_payload_is_valid_then_create_category_and_return_201(self) -> None:
        url = f'/api/categories/'
        response = self.client.post(
            url,
            data={
            "name": 'Movie',
            "description": "Movie Description",
        })
        assert response.status_code == status.HTTP_201_CREATED

    def test_when_payload_is_invalid_for_update_view_then_return_400(self) -> None:
        url = f'/api/categories/123123123/' #UUID inválido
        response = self.client.put(
            url,
            data={
                "name": '',
                "description": "Movie Description",
                # is_active missing
            })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
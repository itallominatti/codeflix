from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        url = "/api/categories/"
        response = self.client.get(url)

        expected_data = [
                {
                    "id": "UUID",
                    "name": "Movie",
                    "description": "Movie Description",
                    "is_active": True
                },
                {
                    "id": "UUID",
                    "name": "Serie",
                    "description": "Serie Description",
                    "is_active": True
                },
            ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

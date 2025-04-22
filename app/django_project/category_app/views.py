from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request):
        return Response(
            status=status.HTTP_200_OK,
            data=[
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
        )

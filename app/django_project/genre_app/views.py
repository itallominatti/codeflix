from uuid import UUID


from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from app.core.category.application.use_cases.list_category import ListCategoryResponse
from app.core.genre.application.use_cases.list_genre import ListGenre
from app.django_project.genre_app.repository import DjangoOrmGenreRepository
from app.django_project.genre_app.serializers import ListGenreOutputSeralizer


# Create your views here.
class GenreViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request: Request) -> Response:
        use_case = ListGenre(
            repository=DjangoOrmGenreRepository()
        )
        output: ListGenre.Output = use_case.execute(
            input=ListGenre.Input()
        )
        response_serializer = ListGenreOutputSeralizer(output)

        return Response(
            status=status.HTTP_200_OK,
            data=response_serializer.data
        )


    @staticmethod
    def retrieve(request: Request, pk=None) -> Response:
        ...

    @staticmethod
    def create(request: Request) -> Response:
        ...
    @staticmethod
    def update(request: Request, pk=None) -> Response:
        ...

    @staticmethod
    def delete(request: Request, pk=None) -> Response:
        ...

    @staticmethod
    def patch(request: Request, pk=None) -> Response:
        ...
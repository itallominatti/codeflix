from logging import raiseExceptions
from uuid import UUID

from app.core.genre.application.use_cases.create_genre import CreateGenre
from app.core.genre.application.use_cases.delete_genre import DeleteGenre
from app.core.genre.application.use_cases.update_genre import UpdateGenre
from app.django_project.category_app.repository import DjangoORMCategoryRepository
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from app.core.category.application.use_cases.list_category import ListCategoryResponse
from app.core.genre.application.use_cases.list_genre import ListGenre
from app.core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound, GenreNotFound

from app.django_project.genre_app.repository import DjangoOrmGenreRepository
from app.django_project.genre_app.serializers import ListGenreOutputSeralizer, DeleteGenreInputSerializer, \
    UpdateGenreInputSerializer
from app.django_project.genre_app.serializers import CreateGenreRequestSerializer, CreateGenreResponseSerializer

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
        serializer = CreateGenreRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateGenre.Input(**serializer.validated_data)
        use_case = CreateGenre(
            repository=DjangoOrmGenreRepository(),
            category_repository=DjangoORMCategoryRepository()
        )
        try:
            output: CreateGenreResponseSerializer = use_case.execute(input=input)
        except (InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(err)}
            )

        return Response(
            status=status.HTTP_201_CREATED,
            data=CreateGenreResponseSerializer(output).data
        )

    @staticmethod
    def update(request: Request, pk=None) -> Response:
        request_data = UpdateGenreInputSerializer(
            data={
                **request.data,
                "id": pk
            }
        )
        request_data.is_valid(raise_exception=True)

        input = UpdateGenre.Input(
            **request_data.validated_data
        )
        use_case = UpdateGenre(
            repository=DjangoOrmGenreRepository(),
            category_repository=DjangoORMCategoryRepository()
        )
        try:
            use_case.execute(input)
        except (GenreNotFound,RelatedCategoriesNotFound) as err:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(err)}
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )




    @staticmethod
    def delete(request: Request, pk: UUID =None) -> Response:
        request_data = DeleteGenreInputSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)

        input = DeleteGenre.Input(**request_data.validated_data)
        use_case = DeleteGenre(
            repository=DjangoOrmGenreRepository()
        )
        try:
            use_case.execute(input)
        except GenreNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @staticmethod
    def patch(request: Request, pk=None) -> Response:
        ...
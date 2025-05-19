from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from app.core.category.application.exceptions import CategoryNotFound
from app.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from app.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from app.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
)
from app.core.category.application.use_cases.list_category import (
    ListCategoryRequest,
    ListCategory,

)
from app.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from app.django_project.category_app.repository import DjangoORMCategoryRepository
from app.django_project.category_app.serializers import ListCategoryResponseSerializer, \
    RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer, CreateCategoryRequestSerializer, \
    CreateCategoryResponseSerializer, UpdateCategoryRequestSerializer, DeleteCategoryRequestSerializer, \
    PatchCategoryRequestSerializer


# Create your views here.
class CategoryViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request: Request) -> Response:
        order_by = request.query_params.get('order_by', "name")
        current_page = int(request.query_params.get("current_page", 1))
        input = ListCategoryRequest()
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        response = use_case.execute(request=ListCategoryRequest(
            order_by=order_by,
            current_page=current_page
        ))

        serializer = ListCategoryResponseSerializer(instance=response)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )
    @staticmethod
    def retrieve(request: Request, pk=None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True
                            )
        use_case = GetCategory(repository=DjangoORMCategoryRepository())
        try:
            result = use_case.execute(
                request=GetCategoryRequest(id=serializer.validated_data["id"]))
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        category_output = RetrieveCategoryResponseSerializer(instance=result)
        return Response(
            status=status.HTTP_200_OK,
            data=category_output.data
        )

    @staticmethod
    def create(request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateCategory(repository=DjangoORMCategoryRepository())
        response = use_case.execute(
            request=CreateCategoryRequest(**serializer.validated_data)
        )

        response = CreateCategoryResponseSerializer(instance=response)
        return Response(
            data=response.data,
            status=status.HTTP_201_CREATED
        )
    @staticmethod
    def update(request: Request, pk=None) -> Response:
        serializer = UpdateCategoryRequestSerializer(
            data={
                **request.data,
                "id": pk
            })
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(request=input)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @staticmethod
    def delete(request: Request, pk=None) -> Response:
        serializer = DeleteCategoryRequestSerializer(
            data={"id": pk}
        )
        serializer.is_valid(raise_exception=True)

        use_case = DeleteCategory(
            repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=DeleteCategoryRequest(
                **serializer.validated_data
            ))
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @staticmethod
    def patch(request: Request, pk=None) -> Response:
        serializer = PatchCategoryRequestSerializer(
            data={
                **request.data,
                "id": pk
            },
            partial=True)
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(request=input)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
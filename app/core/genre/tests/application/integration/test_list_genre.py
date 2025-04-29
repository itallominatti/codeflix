from app.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from app.core.genre.application.use_cases.list_genre import ListGenre, GenreOutput
from app.core.genre.domain.genre import Genre
from app.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository

from app.core.category.domain.category import Category



class TestListGenre:
    def test_list_genres_with_associated_categories(self):
        category_repository = InMemoryCategoryRepository()

        movie_category = Category(
            name="Movie"
        )
        documentary_category = Category(
            name="Documentary"
        )

        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        genre_repository = InMemoryGenreRepository()
        genre = Genre(
            name="Drama",
            categories={movie_category.id, documentary_category.id}
        )
        genre_repository.save(genre)

        use_case = ListGenre(repository=genre_repository)

        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    name="Drama",
                    id=genre.id,
                    is_active=True,
                    categories={movie_category.id, documentary_category.id}
                )
            ]
        )

    def test_list_without_genres(self):
        genre_repository = InMemoryGenreRepository()
        use_case = ListGenre(repository=genre_repository)

        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 0
        assert output == ListGenre.Output(
            data=[]
        )

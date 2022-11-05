from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from ...models import Categories, Comment, Genres, GenreTitle, Review, Title

User = get_user_model()

ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить данные из файла CSV,
сначала удалите базу данных db.sqlite3.
Затем запустите `python manage.py migrate` для новой пустой
база данных с таблицами"""


class Command(BaseCommand):

    def handle(self, *args, **options):

        if (
            Categories.objects.exists()
            and Comment.objects.exists()
            and Genres.objects.exists()
            and Review.objects.exists()
            and Title.objects.exists()
            and GenreTitle.objects.exists()
        ):
            print('данные уже загружены... выход.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загружаются данные пользователей")

        with open('static/data/users.csv', encoding='utf-8') as csvfile:
            for row in DictReader(csvfile):
                User.objects.get_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role']
                )

        print("Загружаются данные таблицы категорий")

        with open('static/data/category.csv', encoding='utf-8') as csvfile:
            for row in DictReader(csvfile):
                Categories.objects.get_or_create(
                    name=row['name'],
                    slug=row['slug']
                )

        print("Загружаются данные таблицы жанров")

        with open('static/data/genre.csv', encoding='utf-8') as csvfile:
            for row in DictReader(csvfile):
                Genres.objects.get_or_create(
                    name=row['name'],
                    slug=row['slug']
                )

        print("Загружаются данные таблицы тайтлов")

        with open('static/data/titles.csv', encoding='utf-8') as csvfile:
            for row in DictReader(csvfile):
                Title.objects.get_or_create(
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category']
                )

        print("Загружаются данные таблицы жанров/тайтлов")

        with open('static/data/genre_title.csv') as csvfile:
            for row in DictReader(csvfile):
                title = Title.objects.get(id=row['title_id'])
                title.genre.add(row['genre_id'])

        print("Загружаются данные таблицы отзывов")

        with open('static/data/review.csv', encoding='utf-8') as csvfile:
            for row in DictReader(csvfile):
                Review.objects.get_or_create(
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date']
                )

        print("Загружаются данные таблицы комментариев")

        with open('static/data/comments.csv', encoding='utf-8') as csvfile:
            for row in DictReader(csvfile):
                Comment.objects.get_or_create(
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date']
                )

        print("Загрузка завершена")

# Проект YaMDb
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/downloads/release/python-379/) [![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/) [![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/) [![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/) [![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/) [![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/) [![Workflow](https://github.com/Rezenhorn/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/Rezenhorn/yamdb_final/actions/workflows/yamdb_workflow.yml)

## Описание:

- Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор. Пользователи могут оставлять отзывы и ставить произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется рейтинг.
- В проекте предусмотрен API. Полный список операций доступен по [ссылке](http://localhost/redoc/) (работает на запущенном сервере).
- В проекте реализована аутентификация по JWT-токену.

## Как запустить проект:

### Клонировать репозиторий и перейти в него:
```
git clone https://github.com/Rezenhorn/infra_sp2.git
```
### Создать файл .env в папке infra/ и заполнить его в соответствии с примером (файл .env.example):
### Из папки infra/ запустить Docker:
```
docker-compose up -d --build
```
### Выполнить миграции, создать суперпользователя, собрать статику:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
### Загрузить тестовые данные:

```
docker-compose exec web python manage.py loaddata fixtures.json
```
## Остановить собранные контейнеры:
```
docker-compose down -v
```
## Регистрация пользователя:

- Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
- Сервис отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
- Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен). Токен позволяет работать с API проекта, необходимо отправлять токен с каждым запросом.
- Токен должен обновляться через повторную передачу username и кода подтверждения. Срок действия токена - одни сутки.

## Авторы проекта:

- [Дмитрий Фомичев](https://github.com/Rezenhorn): Auth, Users, JWT-tokens, Docker
- [Мария Прохорова](https://github.com/aifrel): Categories, Genres, Titles
- [Дмитрий Кузнецов](https://github.com/QuznetsovDi): Review, Comments, импорт csv-файлов

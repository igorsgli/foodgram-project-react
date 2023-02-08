![example workflow](https://github.com/igorsgli/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

server_name (IP or domain name): 158.160.54.226

Адрес сайта:
```
http://158.160.59.12/
```

### Проект: Foodgram

Описание проекта:

Проект **Foodgram** - онлайн-сервис «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


Стек:

```
Python, Django, Django REST framework, PostgreSQL, Gunicorn, Nginx, Docker, Docker Hub
```

Скопируйте файлы docker-compose.yml, nginx.conf и папку docs из папки проекта infra на сервер:

```
scp -r ~/Dev/foodgram-project-react/infra/docker-compose.yml igor@158.160.59.12:~/
```

```
scp -r ~/Dev/foodgram-project-react/infra/nginx.conf igor@158.160.59.12:~/
```

```
scp -r ~/Dev/foodgram-project-react/infra/docs igor@158.160.59.12:~/
```

Файл переменных окружения .env на сервере создается скриптом в foodgram_workflow.yml:

```
jobs:
...
    deploy:
    ...
        touch .env
        echo SECRET_KEY=${{ secrets.SECRET_KEY }} >> .env  # Secrets ключ на GITHUB Actions
        echo DEBUG=False >> .env
        echo DB_SQLITE=False >> .env
        echo HOST=${{ secrets.HOST }} >> .env  # Secrets ключ на GITHUB Actions
        echo DB_ENGINE=${{ secrets.DB_ENGINE }} >> .env  # Secrets ключ на GITHUB Actions
        echo DB_NAME=${{ secrets.DB_NAME }} >> .env  # Secrets ключ на GITHUB Actions
        echo POSTGRES_USER=${{ secrets.POSTGRES_USER }} >> .env  # Secrets ключ на GITHUB Actions
        echo POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }} >> .env  # Secrets ключ на GITHUB Actions
        echo DB_HOST=${{ secrets.DB_HOST }} >> .env  # Secrets ключ на GITHUB Actions
        echo DB_PORT=${{ secrets.DB_PORT }} >> .env  # Secrets ключ на GITHUB Actions
```

Шаблон наполнения env-файла:

```
SECRET_KEY='secret_key' # секретный ключ Django
```

```
DEBUG=False # включение/отключение режима отладки
```

```
DB_SQLITE=False # выбор базы данных (если True - sqlite3, иначе - postgresql)
```

```
HOST='158.160.59.12' # IP адрес сервера
```

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
```

```
DB_NAME=postgres # имя базы данных
```

```
POSTGRES_USER=postgres # логин для подключения к базе данных
```

```
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
```

```
DB_HOST=db # название сервиса (контейнера)
```

```
DB_PORT=5432 # порт для подключения к БД
```

Создайте коммит и выполните push проекта:

```
git add .
```

```
git commit -m 'комментарий'
```

```
git push
```

После развертывания приложения на сервере:

Создайте миграции:

```
docker-compose exec django python manage.py makemigrations
```

```
docker-compose exec django python manage.py migrate
```

Создайте суперпользователя:

```
docker-compose exec django python manage.py createsuperuser
```

Настройте сбор статики:

```
docker-compose exec django python manage.py collectstatic --no-input
```

Загрузите данные в базу для таблиц Ингредиенты и Теги:

```
docker-compose exec django python manage.py load
```

Для дальнейшей работы с сайтом ознакомьтесь с документацией приложения:

```
http://158.160.59.12/api/docs/
```

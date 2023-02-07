![example workflow](https://github.com/igorsgli/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

server_name (IP or domain name): 158.160.59.12
```
http://158.160.59.12/
```

### Проект: Foodgram

Описание проекта:

```
Проект **YaMDb** собирает отзывы пользователей на различные произведения. Сами произведения в YaMDb не хранятся.
Произведения делятся на категории и жанры из списка предустановленныых.
Добавлять произведения, категории и жанры может только администратор.
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется рейтинг.
Пользователи могут также оставлять комментарии к отзывам.
```

Стек:

```
Python, Django, Django REST framework, PostgreSQL, Gunicorn, Nginx, Docker, Docker Hub
```

Скопируйте файлы docker-compose.yaml и nginx/default.conf из проекта на сервер:

```
scp -r ~/Dev/yamdb_final/infra/docker-compose.yaml backend@62.84.124.124:~/
```

```
scp -r ~/Dev/yamdb_final/infra/nginx backend@62.84.124.124:~/
```

Создайте и настройте файл переменных окружения .env на сервере:

```
touch .env
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
HOST='62.84.124.124' # IP адрес сервера
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

Выполните миграции:

```
docker-compose exec web python manage.py migrate
```

Создайте суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Настройте сбор статики:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Для заполнения базы данных ознакомьтесь с документацией приложения:

```
http://62.84.124.124/redoc/
```


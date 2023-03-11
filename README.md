![foodgram_workflow](https://github.com/YaMaxPy/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Проект «Foodgram»
### Описание
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Сайт:
http://51.250.7.53/ или http://skyline.sytes.net/

### Ресурсы API Foodgram
- API документация доступна по ссылке (создана с помощью redoc): http://skyline.sytes.net/api/docs/

### Настройка приложения для работы с базой данных Postgres
Для подключения и выполненя запросов к базе данных необходимо создать и заполнить файл '.env' с переменными окружения в папке './infra/'.

Шаблон для заполнения файла '.env':

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:YaMaxPy/foodgram-project-react.git
```
```
cd foodgram-project-react
```
Cоздать и активировать виртуальное окружение:
```
python -m venv env
```
```
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
cd backend
```
```
pip install -r requirements.txt
```

Запустить проект:
Из папки "./infra/" выполнить команду создания и запуска контейнеров:
```
docker compose up -d --build
```
После успешного запуска контейнеров выполнить миграции:
```
docker compose exec backend python manage.py makemigrations
```
```
docker compose exec backend python manage.py migrate
```
Создать суперюзера:
```
docker compose exec backend python manage.py createsuperuser
```
Собрать статику:
```
docker compose exec backend python manage.py collectstatic --no-input
```
Заполнить базу данных из csv файла с данными:
```
docker compose exec backend python manage.py load_data --paths data/ingredients.csv --models Ingredient
```

### Технологии
Python 3.7.9, Django 3.2, Django REST Framework 3.12.4, Docker, PostgreSQL, nginx, gunicorn.

### Авторы проекта
Backend: Максим Радченко - https://github.com/YaMaxPy
Frontend: Yandex.Practicum
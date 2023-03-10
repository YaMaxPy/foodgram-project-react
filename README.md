![foodgram_workflow](https://github.com/YaMaxPy/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Проект «Foodgram»
### Описание


### Ресурсы API Foodgram
- Ресурс auth: аутентификация.
- Ресурс users: пользователи.


### Пользовательские роли и права доступа
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям, может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

### Регистрация новых пользователей
- Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
- Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
- Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
- В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом. 
- После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).

### Настройка приложение для работы с базой данных Postgres
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
git clone git@github.com:YaMaxPy/yamdb_final.git
```
```
cd yamdb_final
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
cd api_yamdb
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
docker compose exec web python manage.py migrate
```
Создать суперюзера:
```
docker compose exec web python manage.py createsuperuser
```
Собрать статику:
```
docker compose exec web python manage.py collectstatic --no-input
```

### Заполнение базы данных:
Скопировать файл с дампом базы данных из папки "./infra/" в контейнер:
```
docker cp fixtures.json infra_web_1:/app/fixtures.json
```
Заполнить базу данных из файла с дампом:
```
docker compose exec web python manage.py loaddata fixtures.json
```

### Технологии
Python 3.7.9, Django 3.2, Django REST Framework 3.12.4, Simple JWT 4.7.2, Docker, PostgreSQL, nginx, gunicorn.

### Авторы проекта
Максим Радченко - https://github.com/YaMaxPy
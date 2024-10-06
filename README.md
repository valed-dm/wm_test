# wm_test

Junior Python Developer Test Task for Workmate.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Настройки

Приложение выполнено с учетом требований production-ready, настроен CI, использован RUFF, pre-commit hook.
Для запуска из скачанного каталога нужно выполнить merge_production_dotenvs_in_dotenv.py для создания .env файла,
запустить скрипт flushdb.sh для создания БД, добавить строку подключения к база данных:
(пример: DATABASE_URL=postgresql://dmvaled:dmvaled_default@127.0.0.1:5432/wm_test), поменять
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False) на default=True.

Докеризация:

- docker compose -f docker-compose.production.yml build
- docker compose up -d
- docker compose -f docker-compose.production.yml run --rm django python manage.py migrate
- docker compose -f docker-compose.production.yml run --rm django python manage.py createsuperuser

Запуск готовых образов из Docker Hub:

- docker compose -f docker-compose.yml pull
- docker compose up -d
- docker compose -f docker-compose.yml run --rm django python manage.py migrate

[<img src="docs/images/img_20.png" width="600"/>]()

Документация:

http://127.0.0.1/api/docs/

## ТЗ

API - общий список, детализированный просмотр, фильтр по параметру (порода), перечень параметров (порода),
рейтинг участников. CRUD: (участники и рейтинг) - добавление, полное изменение, частичное изменение, удаление.

Наложенные ограничения: Просмотр документации доступен всем пользователям, доступ к API после получения JWT-токена.
Время жизни токенов: 1 час, 1 сутки. Получить токен можно после авторизации на сайте (email-password)
с последующим запросом токена http://127.0.0.1/api/docs/#/token/token_create путем передачи регистрационных данных.

Дополнительные ограничения: полное изменение, частичное изменение, удаление доступно владельцу записи.
Голосование за свою запись блокировано. Повторное голосование блокировано. Пользователь не может использовать
несколько одинаковых кличек.

В то же время уникальным в общем перечне является только описание - т.е. в нем могут присутствовать сочетания
одинаковых кличек, пород, возрастов, цветов, что в некотором плане соответствует здравому смыслу - и в первую очередь ТЗ.

Соответствующим образом реализована и база данных с целью экономии ресурсов.

## Тестирование

Тестирование проводилось вручную. Полностью покрыты тестами модели (по готовому шаблону, интересное решение).
Приведен пример тестирования сериалайзеров. Для полного покрытия нужно дополнительное время.
Есть пример данных для ручной подстановки (/cat_expo/tests/test_data.txt).

## Скриншоты

[<img src="docs/images/img_01.png" width="300"/>]()

[<img src="docs/images/img_02.png" width="300"/>]()

[<img src="docs/images/img_03.png" width="300"/>]()

[<img src="docs/images/img_04.png" width="300"/>]()

[<img src="docs/images/img_05.png" width="300"/>]()

[<img src="docs/images/img_06.png" width="300"/>]()

[<img src="docs/images/img_07.png" width="300"/>]()

[<img src="docs/images/img_08.png" width="300"/>]()

[<img src="docs/images/img_09.png" width="800"/>]()

[<img src="docs/images/img_10.png" width="800"/>]()

[<img src="docs/images/img_11.png" width="800"/>]()

[<img src="docs/images/img_12.png" width="300"/>]()

[<img src="docs/images/img_13.png" width="300"/>]()

[<img src="docs/images/img_14.png" width="300"/>]()

[<img src="docs/images/img_15.png" width="300"/>]()

[<img src="docs/images/img_16.png" width="300"/>]()

[<img src="docs/images/img_17.png" width="300"/>]()

[<img src="docs/images/img_18.png" width="150"/>]()

[<img src="docs/images/img_19.png" width="300"/>]()

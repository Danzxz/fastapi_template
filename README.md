# Шаблон структуры backend приложения

## Архитектура шаблона

![](/docs/dependency_rules.drawio.png)

## Dependency rule

В шаблоне используется подход [Clean architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html).
Для разработки/доработки сервиса нужно понимание чистой архитектуры и правил зависимостей её слоев.

## Использование шаблона
Для использования шаблона необходимо инициировать новый репозиторий, используя следующие настройки:
1. В разделе "Initialize this repository with" выберите опцию "Use this template".
2. Выберите этот шаблонный репозиторий из списка.
3. Нажмите "Create repository".

## Автомиграции
### Создание миграций
Для создания миграций необходимо выполнить команду внутри контейнера или локально
```zsh
alembic revision --autogenerate -m "$name"
```
### Применение миграций
Миграции применяются автоматически в контейнере migrations.


##  Стек
Основной стек состоит из:

- FastAPI
- SQLAlchemy
- Alembic
- Dependency-injector
- loguru
- Pydantic
- pytest
- pre-commit
- mypy

## Python зависимости
Python зависимости выкачиваются из корпоротивного [nexus](https://nexus.itnap.ru)
За доступом обращаться к:
* [a.shkil](https://gitlab.itnap.ru/a.shkil)

##### Обращаю внимание, что стек может изменяться в зависимости от нужного шаблона

##### В любом проекте обязательно требуется использование pre-commit

```zsh
pre-commit install 
```
```zsh
pre-commit run --all-files
```

Используемые линтеры:

- isort
- black
- autoflake
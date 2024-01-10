# Учебный проект по системному анализу

Разработка **REST API** с помощью `Python`, `FastAPI`, `PostgreSQL` и `Docker`

## Описание

В качестве идеи для проекта лежит разработка CRM-системы:

- Заказчик CRM - Агенство инвестиционных проектов (далее Агенство)

- Агенство подчиняется Министерству инвестиций. Также плотно работает с Министерством экономического развития и Министерством финансов

- Сейчас в Агенстве используют большой Эксель файл для ведения клиентов и проектов. Уже не могут масштабировать этот файл. Он стал слишком большим и с большим количеством полей. Невозможно одновременно  работать нескольким сотрудникам

- В Агенстве смотрели универсальные CRM. Но они больше заточены под продажи, потоки клиентов, воронки продаж. Агенству это не подходит. У них свои специфические бизнес-процессы

- Также Агенством рассматривался опыт других регионов. Понравилось решение Тюменьской области. Там сделали CRM под себя и очень довольны

## Артефакты

- [Первичная анкета с вопросами/ответами](/docs/questions.md)
- [Иерархия стейкхолдеров](./docs/images/orgs.jpg)
- [Статусная модель проекта](./docs/images/states_projects.png)
- [Логическая модель](./docs/images/erd.png)
- [Логическая модель на dbdocs.io](https://dbdocs.io/realSiML/sa_invest)
- [Логическая модель schema.dbml](./docs/schema.dbml)

## Использование

1. `cp .env.example .env`
2. `docker-compose up -d --build`
3. `docker-compose exec invest_crm_api alembic upgrade head`
4. `http://localhost:8000/docs`

## TODO
- [ ] Эндпоинты
  - [ ] `/users/{user_id}/projects`
  - [ ] `/projects/{project_id}/users`
  - [ ] `/support/{support_id}/decisions`
  - [ ] `/projects/{project_id}/support`
  - [ ] `/projects/{project_id}/support/{support_id}/decisions`
- [ ] Использовать FastAPI dependencies для валидации данных
- [ ] Зарефакторить boilerplate код в `router.py` и `service.py`

## Библиография

### FastAPI

- https://github.com/zhanymkanov/fastapi-best-practices
- https://github.com/zhanymkanov/fastapi_production_template
- https://github.com/zhanymkanov/fastapi-best-practices/issues/4

### REST API

- https://restapitutorial.ru/
- https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design
- https://developer.mozilla.org/ru/docs/Glossary/Idempotent

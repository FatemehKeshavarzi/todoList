# TODO LIST

### install dependencies

```sell
poetry install
```

### run

```shell
poetry run python main.py
```

### install postgres image

```shell
docker pull postgres:16-alpine
```

### run postgres

```shell
docker run -d --name postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pwd -e POSTGRES_DB=db -p 127.0.0.1:5000:5432 postgres:16-alpine
```

add volume option for data persistence

```shell
-v postgres_data:/var/lib/postgresql/data
```

### alembic migration

migrate

```shell
poetry run alembic revision --autogenerate -m "message"
```

update database

```shell
poetry run alembic upgrade head
```

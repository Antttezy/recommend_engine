FROM python:3.13-alpine AS build-api
WORKDIR /src

RUN apk add --no-cache uv

COPY pyproject.toml uv.lock ./
COPY api/pyproject.toml api/pyproject.toml

RUN uv sync --frozen --project=api --dev

COPY api api
RUN source .venv/bin/activate && sh api/grpc/compile.sh


FROM python:3.13-alpine AS build
WORKDIR /src

RUN apk add --no-cache uv

COPY pyproject.toml uv.lock ./
COPY api/pyproject.toml api/pyproject.toml
COPY core/pyproject.toml core/pyproject.toml
COPY infrastructure/pyproject.toml infrastructure/pyproject.toml
COPY migrator/pyproject.toml migrator/pyproject.toml

RUN uv sync --frozen --project=migrator

COPY --from=build-api /src/api api
COPY core core
COPY infrastructure infrastructure
COPY migrator migrator


FROM python:3.13-alpine
WORKDIR /app

COPY --from=build /src /app

ENV PYTHONPATH=/app
CMD [".venv/bin/python", "-m", "migrator.entrypoint"]

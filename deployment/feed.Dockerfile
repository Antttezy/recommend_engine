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
COPY feed/pyproject.toml feed/pyproject.toml
COPY infrastructure/pyproject.toml infrastructure/pyproject.toml

RUN uv sync --frozen --project=feed

COPY --from=build-api /src/api api
COPY core core
COPY feed feed
COPY infrastructure infrastructure


FROM python:3.13-alpine
WORKDIR /app

COPY --from=build /src /app

ENV PYTHONPATH=/app
EXPOSE 8000
CMD [".venv/bin/python", "-m", "feed.main"]

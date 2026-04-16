FROM python:3.13-alpine AS build
WORKDIR /src
RUN apk add uv

COPY pyproject.toml uv.lock ./
COPY core/pyproject.toml core/pyproject.toml
COPY inbox/pyproject.toml inbox/pyproject.toml

RUN uv sync --frozen --project=inbox

COPY core core
COPY inbox inbox


FROM python:3.13-alpine
WORKDIR /app

COPY --from=build /src /app

ENV PYTHONPATH=/app
CMD [".venv/bin/python", "-m", "inbox.main"]

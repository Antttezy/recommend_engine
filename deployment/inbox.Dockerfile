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

# For actual librdkafka version
RUN echo "@edge-main https://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "@edge-comm https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

RUN apk add --no-cache uv
RUN apk add --no-cache gcc musl-dev
RUN apk add --no-cache librdkafka@edge-comm librdkafka-dev@edge-comm

COPY pyproject.toml uv.lock ./
COPY api/pyproject.toml api/pyproject.toml
COPY core/pyproject.toml core/pyproject.toml
COPY inbox/pyproject.toml inbox/pyproject.toml
COPY infrastructure/pyproject.toml infrastructure/pyproject.toml

RUN uv sync --frozen --project=inbox

COPY --from=build-api /src/api api
COPY core core
COPY inbox inbox
COPY infrastructure infrastructure


FROM python:3.13-alpine
WORKDIR /app

# For actual librdkafka version
RUN echo "@edge-main https://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "@edge-comm https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

RUN apk add --no-cache librdkafka@edge-comm

COPY --from=build /src /app

ENV PYTHONPATH=/app
CMD [".venv/bin/python", "-m", "inbox.main"]

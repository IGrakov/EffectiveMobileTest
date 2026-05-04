ARG PYTHON_VERSION=3.14
ARG ALPINE_VERSION=3.23

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS builder

WORKDIR /build

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    curl

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main && \
    find /usr/local -type d -name "__pycache__" -exec rm -rf {} + && \
    rm -rf /usr/local/lib/python*/site-packages/pip

# ---------------- runtime ----------------

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS runtime

ENV PYTHONUNBUFFERED=1 \
    PATH="${PATH}:/app"

RUN apk add --no-cache libpq

COPY --from=builder /usr/local/ /usr/local/
COPY --from=builder /usr/lib/libpq.* /usr/lib/

WORKDIR /app
COPY ./src ./

# ---------------- dev ----------------

FROM builder AS dev

RUN poetry install --no-root --with dev

WORKDIR /app
COPY pyproject.toml ./
COPY ./src ./src/

WORKDIR /app/src
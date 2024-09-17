FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.8.2

RUN pip3 install --upgrade pip setuptools wheel poetry==${POETRY_VERSION}

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_HOME=/opt/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install

COPY . /app/

RUN poetry install
RUN adduser -D -g '' core_user && chown core_user:core_user -R /app
USER core_user

EXPOSE 8000
CMD ["gunicorn", "--workers", "2", "--timeout", "680", "--log-level", "info", "--bind", "0.0.0.0:8000", "core_application.wsgi"]

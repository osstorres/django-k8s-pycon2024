FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.8.2
ENV DJANGO_SETTINGS_MODULE=analytics_application.settings
ENV DJANGO_CONFIGURATION=Dev

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
RUN adduser -D -g '' analytics_user && chown analytics_user:analytics_user -R /app
USER analytics_user

EXPOSE 8001
CMD ["gunicorn", "--workers", "2", "--timeout", "680", "--log-level", "info", "--bind", "0.0.0.0:8001", "analytics_application.wsgi:application"]


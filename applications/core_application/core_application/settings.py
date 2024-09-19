from pathlib import Path

from configurations import Configuration, values


class Base(Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = "django-insecure-1qbs$d%mrz@0123#))m_#g-qdk$zh@w*e-u^m5009q*sze==q!"

    DEBUG = True

    ALLOWED_HOSTS = []

    BASE_DJANGO_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    LOCAL_APPS = ["monitor", "general", "hello"]
    THIRD_PARTY_APPS = [
        "django_celery_beat",
        "django_celery_results",
        "rest_framework",
        "drf_spectacular",
        "django_filters",
        "corsheaders",
    ]

    INSTALLED_APPS = BASE_DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "core_application.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "core_application.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/5.1/ref/settings/#databases

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    # Default primary key field type
    # https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    STATIC_URL = "static/"

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Celery
    # https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
    # https://pypi.org/project/django-celery-beat/
    # ==========================================
    CELERY_BROKER_URL = values.SecretValue()
    CELERY_RESULT_BACKEND = "django-db"
    CELERY_RESULT_EXTENDED = True
    CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
    CELERY_TASK_SERIALIZER = "pickle"
    CELERY_ACCEPT_CONTENT = ["pickle", "application/json", "application/text"]

    # Rest Framework
    # https://www.django-rest-framework.org/
    # ==========================================
    REST_FRAMEWORK = {
        "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.BasicAuthentication",
            "rest_framework.authentication.SessionAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
        "DEFAULT_FILTER_BACKENDS": (
            "django_filters.rest_framework.DjangoFilterBackend",
        ),
        "TEST_REQUEST_DEFAULT_FORMAT": "json",
        # added custom exception handler
        "JSON_UNDERSCOREIZE": {"no_underscore_before_number": True},
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    }
    SPECTACULAR_SETTINGS = {
        "TITLE": "Core application API",
        "DESCRIPTION": "Core application API",
        "VERSION": "1.0.0",
        "SERVE_INCLUDE_SCHEMA": False,
    }

    CACHE_LOCATION = values.Value("", environ_prefix=None)
    if CACHE_LOCATION:
        CACHES = {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": CACHE_LOCATION,
            }
        }

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": "INFO",
            },
            "core_application": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
        },
    }


class Dev(Base):
    DATABASES = values.DatabaseURLValue(
        "sqlite://:memory:",
        conn_max_age=600,
        conn_health_checks=True,
    )
    CORS_ORIGIN_ALLOW_ALL = True
    ALLOWED_HOSTS = ["*"]
    DEBUG = False

    CELERY_BEAT_SCHEDULE = {
        'hello_task': {
            'task': 'hello.tasks.hello_task',
            'schedule': 5.0,  # Every 5 seconds
        },
    }


class Testing(Dev):

    # Celery
    # ==========================================
    CELERY_BROKER_URL = ""
    CELERY_RESULT_BACKEND = ""
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_TASK_ALWAYS_EAGER = True
    BROKER_BACKEND = "memory"
    CELERY_DELAY_TASK = False
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

import os
from pathlib import Path
print(">>> SETTINGS LOADED: delivery_api.settings")
print(">>> DEBUG =", os.getenv("DEBUG"))
print(">>> ALLOWED_HOSTS(raw) =", os.getenv("ALLOWED_HOSTS"))
print(">>> CORS_ALLOWED_ORIGINS =", [
    "https://delivery-api-cocobambu.vercel.app",
])

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-_^e1*o=6!nenj+15+p$$h*3x-$3ai(cpa&dr&@kvdruhs6emcu",
)

DEBUG = os.getenv("DEBUG", "0").lower() in ("1", "true", "yes")

raw_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,backend")
ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(",") if h.strip()]

if DEBUG and "0.0.0.0" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("0.0.0.0")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "apps.orders.apps.OrdersConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "delivery_api.middleware_debug.DebugCorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "https://delivery-api-cocobambu.vercel.app",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://delivery-api-cocobambu-.*\.vercel\.app$",
]
ROOT_URLCONF = "delivery_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "delivery_api.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

ORDERS_JSON_PATH = os.getenv("ORDERS_JSON_PATH", str(BASE_DIR / "data" / "pedidos.json"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
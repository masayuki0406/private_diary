from .settings_common import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-y(mlq6@d524x4n#-2&))*3d#%_-vqzrmh)ow&is*(#$ygym(p2"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Logging setting
LOGGING = {
    "version": 1,  # 1固定
    "disable_existing_loggers": False,
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "diary": {"handlers": ["console"], "level": "DEBUG"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "dev",
        }
    },
    "formatters": {
        "dev": {
            "format": "\t".join(
                [
                    "%(asctime)s",
                    "[%(levelname)s]",
                    "%(pathname)s(Line:%(lineno)d)",
                    "%(message)s",
                ]
            )
        }
    },
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

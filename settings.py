import os
import sys
import logging
import environ

BASE_DIR = os.path.dirname(__file__)

environ.Env.read_env('.env')
env = environ.Env()


DEBUG = env.bool('DEBUG')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s P%(process)d %(levelname)s |%(name)s| %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
        'sentry': {
            'level': 'ERROR',
            'formatter': 'verbose',
            'class': 'raven.handlers.logging.SentryHandler',
        },
    },
    'loggers': {
        'lingupp': {
            'handlers': ['console', 'sentry'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('CHATIO')


# Database
DATABASES = {
    'host': env.str('POSTGRES_HOST', default='127.0.0.1'),
    'port': env.int('POSTGRES_PORT', default='5432'),
    'database': env.str('POSTGRES_DB'),
    'user': env.str('POSTGRES_USER'),
    'password': env.str('POSTGRES_PASSWORD'),
}


REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.str('REDIS_PORT')
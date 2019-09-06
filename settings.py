import os
import sys
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
            'format': '%(asctime)s P%(process)d %(levelname)s |%(name)s| %(funcName)s | %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },

    },
    'loggers': {
        'aiohttp.server': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}


# Database
DATABASE = {
    'host': env.str('POSTGRES_HOST', default='127.0.0.1'),
    'port': env.int('POSTGRES_PORT', default='5432'),
    'database': env.str('POSTGRES_DB'),
    'user': env.str('POSTGRES_USER'),
    'password': env.str('POSTGRES_PASSWORD'),
}


REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.str('REDIS_PORT')
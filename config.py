import os

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
OUTPUT_COOKIE = os.getenv('OUTPUT_COOKIE', 'karl')
COOKIE_LIFETIME = os.getenv('COOKIE_LIFETIME', 3600)
COOKIE_DOMAIN = '.sixt.de'

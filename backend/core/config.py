import os


POSTGRES_URL = os.getenv('POSTGRES_URL', 'postgresql://localhost:5432/credit_cards')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CACHE_TTL_SECONDS = int(os.getenv('CACHE_TTL_SECONDS', '900'))

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DEFAULT_ENV = {
    "APP_ENV": "test",
    "APP_HOST": "127.0.0.1",
    "APP_PORT": "8000",
    "JWT_SECRET": "test-secret",
    "DB_HOST": "localhost",
    "DB_PORT": "3306",
    "DB_USER": "test",
    "DB_PASSWORD": "test",
    "DB_NAME": "test_db",
}

for key, value in DEFAULT_ENV.items():
    os.environ.setdefault(key, value)

from app.core.settings import settings  # noqa: E402

settings.APP_ENV = DEFAULT_ENV["APP_ENV"]
settings.APP_HOST = DEFAULT_ENV["APP_HOST"]
settings.APP_PORT = int(DEFAULT_ENV["APP_PORT"])
settings.JWT_SECRET = DEFAULT_ENV["JWT_SECRET"]
settings.DB_HOST = DEFAULT_ENV["DB_HOST"]
settings.DB_PORT = int(DEFAULT_ENV["DB_PORT"])
settings.DB_USER = DEFAULT_ENV["DB_USER"]
settings.DB_PASSWORD = DEFAULT_ENV["DB_PASSWORD"]
settings.DB_NAME = DEFAULT_ENV["DB_NAME"]
settings.MATCHING_ENABLED = True
settings.MATCHING_SYNC_ENABLED = True

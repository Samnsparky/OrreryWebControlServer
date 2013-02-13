import os

DB_URI = os.environ.get("DATABASE_URL", "localhost")
DB_NAME = os.environ.get("DATABASE_NAME", "dev")

DEFAULT_RELAY_STATUS = False
DEFAULT_ORRERY_CONFIG_SPEED = 400

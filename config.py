"""
Terrible excuse for a configuration settings module.

Awful configuration settings module that should be replaced eventually by a
more standard configuration scheme.

@author: Sam Pottinger
@license: GNU GPL v3
"""

import os

DB_URI = os.environ.get("DATABASE_URL", "localhost")
DB_NAME = os.environ.get("DATABASE_NAME", "dev")

DEFAULT_RELAY_STATUS = False
DEFAULT_ORRERY_CONFIG_SPEED = 400

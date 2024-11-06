import logging
import os
from typing import Final

LOG_LEVEL: Final[int] = os.environ.get("LOG_LEVEL", logging.DEBUG)

logging.basicConfig(level=LOG_LEVEL)

import uuid
from datetime import datetime
from typing import TypeVar

ID = TypeVar("ID", bound=uuid.UUID)
DateTime = TypeVar("DateTime", bound=datetime)

"""
!! IMPORTANT !!

DO NOT import this module!
"""

import src.app.logger  # Must be the first
from src.app.api import build_fastapi

api = build_fastapi()

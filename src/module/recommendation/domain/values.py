from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class Score(float):

    def __new__(cls, value):

        if not isinstance(value, float):
            raise TypeError("value must be of type float")

        if not 0 <= value <= 1:
            raise ValueError("value must be between 0 and 1")

        return super().__new__(cls, value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(float))

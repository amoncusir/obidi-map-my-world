from typing import Any, List

from bson.objectid import ObjectId
from pydantic import BaseModel, GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from typing_extensions import Annotated


class GeoJson(BaseModel):
    type: str
    coordinates: List[float]


class ObjectIdPydanticAnnotation(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:

        def from_str(value: str) -> ObjectId:
            return ObjectId(value)

        def to_str(obj: ObjectId) -> str:
            return str(obj)

        from_str_schema = core_schema.chain_schema(
            [core_schema.str_schema(), core_schema.no_info_plain_validator_function(from_str)]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(ObjectId),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(to_str),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


ValidatedObjectId = Annotated[ObjectId, ObjectIdPydanticAnnotation]

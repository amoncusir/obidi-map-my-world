from pydantic import BaseModel, ConfigDict, Field


class FastStreamSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    url: str = Field(...)
    app_id: str = Field(...)
    exchange_name: str = Field(...)
    fail_fast: bool = Field(default=True)

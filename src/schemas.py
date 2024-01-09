from pydantic import BaseModel, ConfigDict, model_validator


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class BasePatchSchema(BaseModel):
    @model_validator(mode="before")
    def check_at_least_one_field(cls, data: dict[str, str | None]):
        if all(field is None for field in data.values()):
            raise ValueError("Хотя бы одно поле должно быть указано")

        return data

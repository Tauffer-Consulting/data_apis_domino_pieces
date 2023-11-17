from pydantic import BaseModel, Field


class InputModel(BaseModel):
    pass


class OutputModel(BaseModel):
    dog_fact: str = Field(
        default="",
        description='A random dog fact.'
    )

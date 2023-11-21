from pydantic import BaseModel, Field
from enum import Enum


class LocationTypes(str, Enum):
    RANDOM = "random"
    AMERICA = "America"
    ATLANTIC_OCEAN = "Atlantic Ocean"
    AFRICA = "Africa"
    ASIA = "Asia"
    PACIFIC_OCEAN = "Pacific Ocean"


class InputModel(BaseModel):
    location: LocationTypes = Field(
        default=LocationTypes.RANDOM,
        description="Retrieve image centered approximately on this location."
    )


class OutputModel(BaseModel):
    image_url: str = Field(
        default=None,
        description='URL of the image.'
    )
    image_base64_string: str = Field(
        default=None,
        description='Image as base64 encoded string.'
    )
    image_file_path: str = Field(
        default=None,
        description='Path to the image file.'
    )


class SecretsModel(BaseModel):
    NASA_API_KEY: str = Field(
        default="DEMO_KEY",
        description="API key for NASA Earth Image API."
    )

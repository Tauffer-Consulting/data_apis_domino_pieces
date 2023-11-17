from pydantic import BaseModel, Field


class InputModel(BaseModel):
    return_string: bool = Field(
        default=True,
        description='Return the image as a base64 encoded string.'
    )
    return_file: bool = Field(
        default=False,
        description='Return the image file.'
    )
    return_url: bool = Field(
        default=False,
        description='Return the image url.'
    )


class OutputModel(BaseModel):
    image_base64_string: str = Field(
        default=None,
        description='Image as base64 encoded string.'
    )
    image_file_path: str = Field(
        default=None,
        description='Path to the image file.'
    )
    image_url: str = Field(
        default=None,
        description='URL to the image.'
    )

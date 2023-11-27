from pydantic import BaseModel, Field
from enum import Enum


class OutputSizeTypes(str, Enum):
    compact = "compact"
    full = "full"


class InputModel(BaseModel):
    symbol: str = Field(
        default="AAPL",
        description="The stock symbol."
    )
    output_size: OutputSizeTypes = Field(
        default=OutputSizeTypes.compact,
        description="The size of the output data. Options are `compact` (100 data points) and full (full-length data). Default is `compact`."
    )
    max_data_points: int = Field(
        default=-1,
        description="The maximum number of data points to return. Default is -1, which returns all data points."
    )


class OutputModel(BaseModel):
    data_file_path: str = Field(
        default="",
        description='Path to the data file.'
    )


class SecretsModel(BaseModel):
    ALPHA_VANTAGE_API_KEY: str = Field(
        description="API key for Alpha Vantage data API."
    )

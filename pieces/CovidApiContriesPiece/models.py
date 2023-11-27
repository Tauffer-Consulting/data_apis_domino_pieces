from pydantic import BaseModel, Field
from typing import List, Optional


class InputModel(BaseModel):
    countries: Optional[List[str]] = Field(default=None)  # This could be an enum but too many countries to list


class OutputInnerModel(BaseModel):
    country: List[str] = Field(alias='Country')
    cases_per_one_million: List[float] = Field(alias='Cases per One Million')


class OutputModel(BaseModel):
    data: OutputInnerModel




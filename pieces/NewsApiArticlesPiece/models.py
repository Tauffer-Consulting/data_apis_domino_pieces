from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from datetime import date


class LanguageType(str, Enum):
    ar = "ar"
    de = "de"
    en = "en"
    es = "es"
    fr = "fr"
    he = "he"
    it = "it"
    nl = "nl"
    no = "no"
    pt = "pt"
    ru = "ru"
    sv = "sv"
    ud = "ud"
    zh = "zh"


class SortByType(str, Enum):
    relevancy = "relevancy"
    popularity = "popularity"
    publishedAt = "publishedAt"


class InputModel(BaseModel):
    query: str = Field(
        default="",
        description="Query to search for."
    )
    from_date: date = Field(
        default="2023-11-01",
        description="From date."
    )
    to_date: date = Field(
        default="2023-11-06",
        description="To date."
    )
    sort_by: SortByType = Field(
        default=SortByType.relevancy,
        description="Sort by. Options are: `relevancy`, `popularity`, `publishedAt`."
    )
    language: LanguageType = Field(
        default=LanguageType.en,
        description="Language to filter by. Options are: `ar`, `de`, `en`, `es`, `fr`, `he`, `it`, `nl`, `no`, `pt`, `ru`, `sv`, `ud`, `zh`."
    )
    number_of_results: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of results to return."
    )


class ArticleModel(BaseModel):
    source: str = Field(description="Source of article.")
    title: str = Field(description="Title of article.")
    author: str = Field(description="Author of article.")
    description: str = Field(description="Description of article.")
    publishedAt: str = Field(description="Date article was published, in ISO format.")
    url: str = Field(description="URL of article.")
    url_to_image: str = Field(default="", description="Image associated with article.")
    content: str = Field(description="Content of article.")


class OutputModel(BaseModel):
    message: str = Field(
        description="Output message to log"
    )
    articles: List[ArticleModel] = Field(
        description="List of articles"
    )


class SecretsModel(BaseModel):
    NEWSAPI_API_KEY: str = Field(
        description="News API API Key"
    )

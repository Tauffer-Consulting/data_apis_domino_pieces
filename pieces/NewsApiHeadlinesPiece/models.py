from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class CategoryType(str, Enum):
    business = "business"
    entertainment = "entertainment"
    general = "general"
    health = "health"
    science = "science"
    sports = "sports"
    technology = "technology"


class CountryType(str, Enum):
    all = "all"
    ae = "ae"
    ar = "ar"
    at = "at"
    au = "au"
    be = "be"
    bg = "bg"
    br = "br"
    ca = "ca"
    ch = "ch"
    cn = "cn"
    co = "co"
    cu = "cu"
    cz = "cz"
    de = "de"
    eg = "eg"
    fr = "fr"
    gb = "gb"
    gr = "gr"
    hk = "hk"
    hu = "hu"
    id = "id"
    ie = "ie"
    il = "il"
    in_ = "in"
    it = "it"
    jp = "jp"
    kr = "kr"
    lt = "lt"
    lv = "lv"
    ma = "ma"
    mx = "mx"
    my = "my"
    ng = "ng"
    nl = "nl"
    no = "no"
    nz = "nz"
    ph = "ph"
    pl = "pl"
    pt = "pt"
    ro = "ro"
    rs = "rs"
    ru = "ru"
    sa = "sa"
    se = "se"
    sg = "sg"
    si = "si"
    sk = "sk"
    th = "th"
    tr = "tr"
    tw = "tw"
    ua = "ua"
    us = "us"
    ve = "ve"
    za = "za"


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


class InputModel(BaseModel):
    query: str = Field(description="Query to search for.")
    category: CategoryType = Field(
        default=CategoryType.general,
        description="Category to filter by. Options are: `business`, `entertainment`, `general`, `health`, `science`, `sports`, `technology`."
    )
    country: CountryType = Field(
        default=CountryType.all,
        description="Country to filter by. Options are: `all`, `ae`, `ar`, `at`, `au`, `be`, `bg`, `br`, `ca`, `ch`, `cn`, `co`, `cu`, `cz`, `de`, `eg`, `fr`, `gb`, `gr`, `hk`, `hu`, `id`, `ie`, `il`, `in`, `it`, `jp`, `kr`, `lt`, `lv`, `ma`, `mx`, `my`, `ng`, `nl`, `no`, `nz`, `ph`, `pl`, `pt`, `ro`, `rs`, `ru`, `sa`, `se`, `sg`, `si`, `sk`, `th`, `tr`, `tw`, `ua`, `us`, `ve`, `za`."
    )
    language: LanguageType = Field(
        default=LanguageType.en,
        description="Language to filter by. Options are: `ar`, `de`, `en`, `es`, `fr`, `he`, `it`, `nl`, `no`, `pt`, `ru`, `sv`, `ud`, `zh`."
    )
    number_of_results: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of results to return"
    )


class ArticleModel(BaseModel):
    source: str = Field(description="Source of article.")
    title: str = Field(description="Title of article.")
    author: str = Field(description="Author of article.")
    description: str = Field(description="Description of article.")
    publishedAt: str = Field(description="Date article was published, in ISO format.")
    url: str = Field(description="URL of article.")
    url_to_image: str = Field(default="", description="Image associated with article.")


class OutputModel(BaseModel):
    message: str = Field(description="Output message to log.")
    articles: List[ArticleModel] = Field(description="List of articles.")


class SecretsModel(BaseModel):
    NEWSAPI_API_KEY: str = Field(description="News API API Key.")

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
    query: str = Field(
        default="",
        description="Query to search for"
    )
    category: CategoryType = Field(
        default=CategoryType.general,
        description="Category to filter by"
    )
    country: CountryType = Field(
        default=CountryType.all,
        description="Country to filter by"
    )
    language: LanguageType = Field(
        default=LanguageType.en,
        description="Language to filter by"
    )
    number_of_results: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of results to return"
    )


class OutputModel(BaseModel):
    message: str = Field(
        description="Output message to log"
    )
    articles: List = Field(
        description="List of articles"
    )


class SecretsModel(BaseModel):
    NEWSAPI_API_KEY: str = Field(
        description="News API API Key"
    )

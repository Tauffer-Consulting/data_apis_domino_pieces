from pydantic import BaseModel, Field
from datetime import date


class InputModel(BaseModel):
    max_number_of_events: int = Field(
        default=10,
        description='Maximum number of events to return.',
        ge=1,
        le=100
    )
    keyword: str = Field(
        default=None,
        description='Keyword to search for.'
    )
    end_date: date = Field(
        default=None,
        description='End date for the search. Must be a future date.'
    )
    city: str = Field(
        default=None,
        description='City to search for.'
    )
    country_code: str = Field(
        default=None,
        description='Country code to search for. Must be a valid ISO 3166-1 alpha-2 code.',
        min_length=2,
        max_length=2
    )


class EventObjectType(BaseModel):
    name: str = Field(
        description='Name of the event type.'
    )
    event_date: date = Field(
        description='Date of the event.'
    )
    event_location: str = Field(
        description='Location of the event.'
    )
    classification: str = Field(
        default=None,
        description='Classification of the event.'
    )
    url: str = Field(
        default=None,
        description='URL of the event type.'
    )
    image_url: str = Field(
        default=None,
        description='Image URL of the event type.'
    )


class OutputModel(BaseModel):
    events: list[EventObjectType] = Field(
        description='List of events.'
    )
    results_formatted: str = Field(
        description='Text with formatted results.'
    )


class SecretsModel(BaseModel):
    TICKETMASTER_API_KEY: str = Field(
        description="API key for the Ticketmaster API."
    )

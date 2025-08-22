from pydantic import BaseModel

class LocationResponse(BaseModel):
    country: str
    city: str

class ErrorResponse(BaseModel):
    error: str

class SuggestResponse(BaseModel):
    suggestions: list[str]


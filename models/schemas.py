from typing import List, Optional
from pydantic import BaseModel, Field


class LocationItem(BaseModel):
    location_name: str
    linear_feet: Optional[float] = None


class AddressItem(BaseModel):
    location_name: str
    full_address: str


class ExtractedLocationsResponse(BaseModel):
    items: List[LocationItem]


class ExtractedAddressesResponse(BaseModel):
    items: List[AddressItem]


class LocationResult(BaseModel):
    page: int
    location_name: str
    full_address: str
    linear_feet: Optional[float]
    maps_url: str


class ProcessPDFResponse(BaseModel):
    success: bool
    message: str
    locations: List[LocationResult]
    total_locations: int = Field(description="Total number of locations extracted")


class HealthResponse(BaseModel):
    status: str
    environment: str
    version: str = "1.0.0"


class ErrorResponse(BaseModel):
    detail: str
    error_type: Optional[str] = None

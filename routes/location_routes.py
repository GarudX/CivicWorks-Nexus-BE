from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, Query, Security
from fastapi.security import APIKeyHeader
from models.schemas import ProcessPDFResponse
from controllers.location_controller import LocationController

router = APIRouter(prefix="/api/v1/locations", tags=["Locations"])
controller = LocationController()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@router.post(
    "/extract",
    response_model=ProcessPDFResponse,
    summary="Extract locations from PDF maps",
    description="""
    Upload PDF files to extract location information:
    - **map_pdf**: Required PDF containing map with location markers
    - **routing_pdf**: Optional PDF containing routing information with addresses
    - **zoom**: Render zoom level (2.0-6.0, default: 4.0) - higher = clearer text
    - **max_pages**: Maximum pages to process (1-200, default: 30)
    
    Returns location names, addresses, linear feet measurements, and Google Maps links.
    
    **Note**: In development mode (ENVIRONMENT=development), returns hardcoded data to save costs.
    """
)
async def extract_locations(
    map_pdf: UploadFile = File(..., description="Map PDF file with locations to extract"),
    routing_pdf: Optional[UploadFile] = File(None, description="Optional routing PDF with addresses"),
    zoom: float = Form(4.0, ge=2.0, le=6.0, description="Render zoom level"),
    max_pages: int = Form(30, ge=1, le=200, description="Maximum pages to process"),
    api_key: str = Security(api_key_header)
) -> ProcessPDFResponse:
    return await controller.process_location_pdfs(
        map_pdf=map_pdf,
        routing_pdf=routing_pdf,
        zoom=zoom,
        max_pages=max_pages
    )

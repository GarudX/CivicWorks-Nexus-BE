from typing import Optional
from fastapi import UploadFile, HTTPException, status
from models.schemas import ProcessPDFResponse
from services.location_service import LocationService
from utils.logger import logger


class LocationController:
    
    def __init__(self):
        self.service = LocationService()
    
    async def process_location_pdfs(
        self,
        map_pdf: UploadFile,
        routing_pdf: Optional[UploadFile] = None,
        zoom: float = 4.0,
        max_pages: int = 30
    ) -> ProcessPDFResponse:
        try:
            logger.info(f"Processing location PDFs - Map: {map_pdf.filename}")
            
            if map_pdf.content_type != "application/pdf":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Map file must be a PDF"
                )
            
            map_pdf_bytes = await map_pdf.read()
            
            routing_pdf_bytes = None
            if routing_pdf:
                if routing_pdf.content_type != "application/pdf":
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Routing file must be a PDF"
                    )
                routing_pdf_bytes = await routing_pdf.read()
                logger.info(f"Routing PDF provided: {routing_pdf.filename}")
            
            locations = await self.service.process_pdfs(
                map_pdf_bytes=map_pdf_bytes,
                routing_pdf_bytes=routing_pdf_bytes,
                zoom=zoom,
                max_pages=max_pages
            )
            
            if not locations:
                logger.warning("No locations extracted from PDFs")
                return ProcessPDFResponse(
                    success=False,
                    message="No locations detected. Try increasing zoom or check PDF quality.",
                    locations=[],
                    total_locations=0
                )
            
            logger.info(f"Successfully processed {len(locations)} locations")
            return ProcessPDFResponse(
                success=True,
                message=f"Successfully extracted {len(locations)} locations",
                locations=locations,
                total_locations=len(locations)
            )
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error processing PDFs: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing PDFs: {str(e)}"
            )

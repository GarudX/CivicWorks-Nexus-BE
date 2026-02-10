import re
import urllib.parse
from typing import List, Dict, Optional
from models.schemas import LocationResult
from repositories.location_repository import LocationRepository
from services.pdf_service import PDFService
from services.openai_service import OpenAIService
from config.settings import get_settings
from utils.logger import logger

settings = get_settings()


class LocationService:
    
    def __init__(self):
        self.repository = LocationRepository()
        self.pdf_service = PDFService()
        self.openai_service = OpenAIService()
    
    @staticmethod
    def google_maps_url(query: str) -> str:
        q = urllib.parse.quote(query or "")
        return f"https://www.google.com/maps/dir/?api=1&destination={q}"
    
    @staticmethod
    def normalize_location_name(name: str) -> str:
        name = name.lower().strip()
        name = re.sub(r'\s+', ' ', name)
        name = re.sub(r'[^a-z0-9\s]', '', name)
        return name
    
    @staticmethod
    def find_best_address_match(location_name: str, address_dict: Dict[str, str]) -> Optional[str]:
        normalized_query = LocationService.normalize_location_name(location_name)
        
        best_match = None
        best_score = 0
        
        for addr_location, address in address_dict.items():
            normalized_addr_loc = LocationService.normalize_location_name(addr_location)
            
            if normalized_query == normalized_addr_loc:
                return address
            
            if normalized_query in normalized_addr_loc or normalized_addr_loc in normalized_query:
                words_query = set(normalized_query.split())
                words_addr = set(normalized_addr_loc.split())
                common = len(words_query & words_addr)
                total = len(words_query | words_addr)
                score = common / total if total > 0 else 0
                
                if score > best_score:
                    best_score = score
                    best_match = address
        
        if best_score > 0.5:
            return best_match
        
        return None
    
    async def process_pdfs(
        self,
        map_pdf_bytes: bytes,
        routing_pdf_bytes: Optional[bytes] = None,
        zoom: float = 4.0,
        max_pages: int = 30
    ) -> List[LocationResult]:
        logger.info(f"Processing PDFs - Environment: {settings.ENVIRONMENT}")
        
        if settings.ENVIRONMENT == "development":
            logger.info("Using development mode with hardcoded data")
            return self._process_development_mode()
        else:
            logger.info("Using production mode with OpenAI API")
            return await self._process_production_mode(
                map_pdf_bytes, routing_pdf_bytes, zoom, max_pages
            )
    
    def _process_development_mode(self) -> List[LocationResult]:
        address_dict = self.repository.get_dev_address_dict()
        dev_locations = self.repository.get_dev_locations()
        
        results = []
        page_num = 1
        
        for location in dev_locations:
            matched_address = self.find_best_address_match(
                location.location_name, address_dict
            )
            
            query = (
                f"{location.location_name} {matched_address}"
                if matched_address
                else location.location_name
            )
            
            results.append(
                LocationResult(
                    page=page_num,
                    location_name=location.location_name,
                    full_address=matched_address if matched_address else "Not found",
                    linear_feet=location.linear_feet,
                    maps_url=self.google_maps_url(query),
                )
            )
        
        logger.info(f"Processed {len(results)} locations in development mode")
        return results
    
    async def _process_production_mode(
        self,
        map_pdf_bytes: bytes,
        routing_pdf_bytes: Optional[bytes],
        zoom: float,
        max_pages: int
    ) -> List[LocationResult]:
        address_dict = {}
        
        if routing_pdf_bytes:
            logger.info("Processing routing PDF for addresses")
            routing_pages = self.pdf_service.pdf_to_images(
                routing_pdf_bytes, zoom, max_pages
            )
            
            for page_num, img in routing_pages:
                data, _ = self.openai_service.extract_addresses_from_page(img)
                for item in data.get("items", []):
                    address_dict[item["location_name"]] = item["full_address"]
            
            logger.info(f"Found {len(address_dict)} addresses in routing PDF")
        
        logger.info("Processing map PDF for locations")
        map_pages = self.pdf_service.pdf_to_images(map_pdf_bytes, zoom, max_pages)
        
        results = []
        for page_num, img in map_pages:
            data, _ = self.openai_service.extract_locations_from_page(img)
            
            for item in data.get("items", []):
                location_name = item["location_name"]
                
                matched_address = None
                if address_dict:
                    matched_address = self.find_best_address_match(
                        location_name, address_dict
                    )
                
                query = matched_address if matched_address else location_name
                
                results.append(
                    LocationResult(
                        page=page_num,
                        location_name=location_name,
                        full_address=matched_address if matched_address else "Not found",
                        linear_feet=item["linear_feet"],
                        maps_url=self.google_maps_url(query),
                    )
                )
        
        logger.info(f"Processed {len(results)} locations in production mode")
        return results

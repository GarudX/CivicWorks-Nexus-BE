import json
from typing import Tuple, Dict, Any
from PIL import Image
from openai import OpenAI
from config.settings import get_settings
from utils.logger import logger
from services.pdf_service import PDFService

settings = get_settings()


class OpenAIService:
    
    LOCATION_SCHEMA = {
        "name": "extracted_locations",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "location_name": {"type": "string"},
                            "linear_feet": {"type": ["number", "null"]},
                        },
                        "required": ["location_name", "linear_feet"],
                    },
                }
            },
            "required": ["items"],
        },
    }
    
    ADDRESS_SCHEMA = {
        "name": "extracted_addresses",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "location_name": {"type": "string"},
                            "full_address": {"type": "string"},
                        },
                        "required": ["location_name", "full_address"],
                    },
                }
            },
            "required": ["items"],
        },
    }
    
    def __init__(self):
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.client = None
            logger.warning("OpenAI client not initialized - API key missing")
    
    def extract_locations_from_page(self, page_image: Image.Image) -> Tuple[Dict[str, Any], str]:
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")
        
        image_url = PDFService.pil_to_data_url(page_image)
        
        prompt = """
You are reading a map screenshot.

Extract ALL visible locations that:
- Look like named places (e.g., "Elliot Norton Park", "Bay Village Garden",
  "Clarendon Street Playlot")
- May have a nearby callout showing "X linear feet"

Rules:
- location_name must match the visible label (fix obvious casing errors).
- linear_feet: return the numeric value if shown.
- If no measurement is visible, return null.
- Do NOT invent or guess locations.
"""
        
        logger.info("Sending location extraction request to OpenAI")
        response = self.client.chat.completions.create(
            model=settings.MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            temperature=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": self.LOCATION_SCHEMA["name"],
                    "schema": self.LOCATION_SCHEMA["schema"],
                    "strict": True,
                }
            },
        )
        
        raw_json = response.choices[0].message.content
        data = json.loads(raw_json)
        logger.info(f"Extracted {len(data.get('items', []))} locations from page")
        return data, raw_json
    
    def extract_addresses_from_page(self, page_image: Image.Image) -> Tuple[Dict[str, Any], str]:
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")
        
        image_url = PDFService.pil_to_data_url(page_image)
        
        prompt = """
You are reading a routing document that lists locations with their full addresses.

Extract ALL location entries that show:
- A location name (e.g., "Union Street Park", "Phillips Street Play Area", "Bay Village Garden")
- A complete address (e.g., "98 Union St, Boston, MA 02129, USA")

Rules:
- location_name: Extract the exact name as shown (before the dash or address)
- full_address: Extract the complete address including street, city, state, zip, and country
- Match the visible text exactly, fixing only obvious OCR errors
- Do NOT invent or guess information
"""
        
        logger.info("Sending address extraction request to OpenAI")
        response = self.client.chat.completions.create(
            model=settings.MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            temperature=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": self.ADDRESS_SCHEMA["name"],
                    "schema": self.ADDRESS_SCHEMA["schema"],
                    "strict": True,
                }
            },
        )
        
        raw_json = response.choices[0].message.content
        data = json.loads(raw_json)
        logger.info(f"Extracted {len(data.get('items', []))} addresses from page")
        return data, raw_json

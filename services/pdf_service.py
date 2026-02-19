import io
import base64
from typing import List, Tuple
from PIL import Image
import pypdfium2 as pdfium


class PDFService:
    
    @staticmethod
    def pdf_to_images(pdf_bytes: bytes, zoom: float, limit: int) -> List[Tuple[int, Image.Image]]:
        pdf = pdfium.PdfDocument(pdf_bytes)
        
        pages = []
        scale = zoom
        
        for i in range(min(len(pdf), limit)):
            page = pdf[i]
            pil_image = page.render(
                scale=scale,
                rotation=0,
            ).to_pil()
            pages.append((i + 1, pil_image.convert("RGB")))
            page.close()
        
        pdf.close()
        return pages
    
    @staticmethod
    def pil_to_data_url(pil_img: Image.Image) -> str:
        buf = io.BytesIO()
        pil_img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/png;base64,{b64}"

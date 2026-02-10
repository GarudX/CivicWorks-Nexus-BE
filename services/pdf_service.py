import io
import base64
from typing import List, Tuple
from PIL import Image
import fitz


class PDFService:
    
    @staticmethod
    def pdf_to_images(pdf_bytes: bytes, zoom: float, limit: int) -> List[Tuple[int, Image.Image]]:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        mat = fitz.Matrix(zoom, zoom)
        
        pages = []
        for i in range(min(len(doc), limit)):
            pix = doc[i].get_pixmap(matrix=mat, alpha=False)
            img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            pages.append((i + 1, img))
        
        doc.close()
        return pages
    
    @staticmethod
    def pil_to_data_url(pil_img: Image.Image) -> str:
        buf = io.BytesIO()
        pil_img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/png;base64,{b64}"

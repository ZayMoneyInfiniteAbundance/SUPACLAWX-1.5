import io
from pathlib import Path
from config import PREVIEW_CACHE_DIR, PDF_PREVIEW_ENABLED


def extract_first_page_as_png(pdf_bytes: bytes, niche_id: str) -> bytes:
    if not PDF_PREVIEW_ENABLED:
        return None
    cache_path = PREVIEW_CACHE_DIR / f"{niche_id}.png"
    if cache_path.exists():
        return cache_path.read_bytes()
    try:
        import fitz
    except ImportError:
        return None
    PREVIEW_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0]
        pix = page.get_pixmap(dpi=100)
        img_bytes = pix.tobytes("png")
        cache_path.write_bytes(img_bytes)
        doc.close()
        return img_bytes
    except Exception:
        return None

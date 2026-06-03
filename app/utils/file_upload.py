from pathlib import Path
from fastapi import HTTPException, UploadFile
import uuid

BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "uploads" / "mango_images"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def get_image_url(filename: str) -> str:
    return f"/uploads/mango_images/{filename}"


async def save_upload_file(file: UploadFile) -> str:
    filename = Path(file.filename).name
    if not filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a filename")

    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    safe_filename = f"{uuid.uuid4().hex}{extension}"
    destination = UPLOAD_DIR / safe_filename

    contents = await file.read()
    destination.write_bytes(contents)

    return safe_filename

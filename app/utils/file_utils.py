import os
import shutil
from typing import Generator
from fastapi import UploadFile

def sanitize_filename(filename: str) -> str:
    """Removes path traversal anomalies and illegal character sets from filenames."""
    base_name = os.path.basename(filename)
    return "".join(c for c in base_name if c.isalnum() or c in "._-").strip()

def save_upload_file(upload_file: UploadFile, destination: str) -> None:
    """Streams incoming multipart bytes directly to disk memory safely."""
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

def get_file_extension(filename: str) -> str:
    """Extracts a normalized, lowercase file extension string."""
    _, ext = os.path.splitext(filename.lower())
    return ext

def remove_file_if_exists(file_path: str) -> None:
    """Cleans up temporary records or orphaned documents from disk storage safely."""
    if os.path.exists(file_path):
        os.remove(file_path)

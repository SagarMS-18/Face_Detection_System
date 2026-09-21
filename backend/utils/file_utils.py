import os
import uuid
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOADS_DIR

def allowed_file(filename):
    """
    Check if the uploaded file has a valid image extension.
    """
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def save_temp_file(file):
    """
    Save an uploaded file temporarily with a unique filename.
    Returns the absolute filepath.
    """
    original_filename = secure_filename(file.filename) or "image.jpg"
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = UPLOADS_DIR / unique_filename
    file.save(str(filepath))
    return str(filepath)

def delete_temp_file(filepath):
    """
    Safely delete a temporary file after processing.
    """
    if filepath and os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Warning: Could not delete temporary file {filepath}: {e}")

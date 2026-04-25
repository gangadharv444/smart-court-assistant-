# ============================================================
# Vidhi-AI | Shared Utility Functions
# ============================================================

import os
import re
import unicodedata


def clean_ai_output(text: str) -> str:
    """Strip leaked training tags, mapping codes, and version
    numbers from GGUF model output."""
    # Remove map:ipc_bns:X.X or similar mapping tags
    text = re.sub(
        r'map:\w[\w_]*(?::\d+\.\d+)?', '', text
    )
    # Remove any remaining version tags like v1.0, v2.1
    text = re.sub(
        r'\bv\d+\.\d+\b', '', text
    )
    # Remove leftover double/triple spaces
    text = re.sub(r'  +', ' ', text)
    # Remove lines that are only whitespace after cleaning
    lines = text.splitlines()
    cleaned_lines = [ln for ln in lines if ln.strip()]
    return '\n'.join(cleaned_lines).strip()


def sanitize_filename(filename: str) -> str:
    """Sanitize an uploaded filename to prevent path traversal
    and special character issues.

    - Strips directory components (path traversal)
    - Removes null bytes
    - Replaces unsafe characters
    - Limits length to 200 characters
    """
    # Take only the basename (strip any directory traversal)
    filename = os.path.basename(filename)
    # Remove null bytes
    filename = filename.replace('\x00', '')
    # Normalize unicode
    filename = unicodedata.normalize('NFKD', filename)
    # Replace any characters that are not alphanumeric, dash,
    # underscore, dot, or space
    filename = re.sub(r'[^\w\-. ]', '_', filename)
    # Collapse multiple underscores/spaces
    filename = re.sub(r'[_ ]{2,}', '_', filename)
    # Limit length
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200 - len(ext)] + ext
    return filename or "uploaded_file.pdf"


def html_escape(text: str) -> str:
    """Escape HTML special characters for safe rendering
    in Streamlit's unsafe_allow_html=True blocks."""
    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def get_upload_dir() -> str:
    """Return a secure upload directory inside the project folder.
    Creates it if it does not exist."""
    upload_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".uploads"
    )
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir

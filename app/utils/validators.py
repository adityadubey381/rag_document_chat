import re
import uuid

def generate_secure_uuid() -> str:
    """Generates standard tracking identification hashes."""
    return str(uuid.uuid4())

def clean_alphanumeric_strings(text: str) -> str:
    """Strips remaining markdown, HTML or raw punctuation artifacts from string sets."""
    if not text:
        return ""
    # Strip non-standard inline ASCII expressions
    return re.sub(r"[^\w\s\.\?\!\-\:\,]", "", text)

def slice_list_into_batches(items: list, batch_size: int) -> Generator[list, None, None]:
    """Chunks arrays into sequential batches for parallel processing."""
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]

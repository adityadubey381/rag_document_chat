import time
import logging
from contextlib import contextmanager
from typing import Generator

logger = logging.getLogger("rag_application")

@contextmanager
def log_execution_time(operation_name: str) -> Generator[None, None, None]:
    """Measures and logs execution duration for performance optimization."""
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        duration = end_time - start_time
        logger.info(f"Performance Profile: Block '{operation_name}' executed in {duration:.4f} seconds.")

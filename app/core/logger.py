import logging

def setup_logger():
    """Configure basic logging for the application."""
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=logging.INFO
    )
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

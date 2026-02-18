from src.logging_config import setup_logging
from src.crawler import run_spider

if __name__ == "__main__":
    setup_logging()
    run_spider("python")

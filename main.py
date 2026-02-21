from src.analysis.data_processing_orchestrator import data_orchestrator
from src.logging_config import setup_logging
from src.crawler import run_spider, get_csv_output_path


def main(field: str):
    setup_logging()

    output_path = get_csv_output_path(field)
    run_spider(field, output_path)
    data_orchestrator(output_path)


if __name__ == "__main__":
    main("python")

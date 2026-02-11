import re
from pathlib import Path


class MainConfig:
    SRC_DIR = Path(__file__).parent.resolve()
    DATA_DIR = SRC_DIR / "data"
    LOGS_DIR = SRC_DIR / "logs"
    CSV_FILENAME_FORMAT = "{field}_vacancies_{timestamp}.csv"

    DOU_URL: str = "https://jobs.dou.ua"
    PYTHON_VACANCIES: str = "/vacancies/?category=Python"

    YEARS_PATTERN = re.compile(
        r"(\d+(?:[.,]\d+)?)\s*(?:\+|plus)?\s*(?:years?|yrs?|y\.?o\.?|роки?|років|р\.)",
        re.IGNORECASE
    )
    MONTHS_PATTERN = re.compile(
        r"(\d+(?:[.,]\d+)?)\s*(?:\+|plus)?\s*(?:months?|mos?|місяц(?:і|ів)?|міс\.?)",
        re.IGNORECASE
    )

    TECH_KEYWORDS = {
        "python", "django", "flask", "fastapi", "aiohttp", "celery", "redis",
        "postgresql", "mysql", "sql", "mongodb", "docker", "kubernetes", "ci/cd",
        "async", "aws", "gcp", "azure", "linux", "git", "pandas", "numpy",
        "pytorch", "tensorflow", "react", "angular", "vue", "javascript",
        "typescript", "html", "css", "drf", "graphql", "rest", "soap", "rabbitmq",
        "kafka", "elasticsearch"
    }

    CRAWLER_SETTINGS = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "LOG_ENABLED": False,
        "FEED_EXPORT_FIELDS": [
            "name", "company_name", "salary", "experience_years", "date",
            "location", "technologies", "url", "company_url", "description"
        ],
    }

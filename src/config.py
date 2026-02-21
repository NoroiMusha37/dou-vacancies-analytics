import re
from pathlib import Path


class MainConfig:
    SRC_DIR = Path(__file__).parent.resolve()
    DATA_DIR = SRC_DIR / "data"
    LOGS_DIR = SRC_DIR / "logs"
    CSV_NAME = "raw_data.csv"

    DOU_URL: str = "https://jobs.dou.ua"
    PYTHON_VACANCIES: str = "/vacancies/?category=Python"

    TECH_KEYWORDS = {
        "python",
        "django",
        "flask",
        "fastapi",
        "aiohttp",
        "celery",
        "redis",
        "postgresql",
        "mysql",
        "sql",
        "mongodb",
        "docker",
        "kubernetes",
        "ci/cd",
        "async",
        "aws",
        "gcp",
        "azure",
        "linux",
        "git",
        "pandas",
        "numpy",
        "pytorch",
        "tensorflow",
        "react",
        "angular",
        "vue",
        "javascript",
        "typescript",
        "html",
        "css",
        "drf",
        "graphql",
        "rest",
        "soap",
        "rabbitmq",
        "kafka",
        "elasticsearch",
    }

    CRAWLER_SETTINGS = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36",
        "LOG_ENABLED": False,
        "FEED_EXPORT_FIELDS": [
            "name",
            "company_name",
            "salary",
            "experience_years",
            "date",
            "location",
            "technologies",
            "url",
            "company_url",
            "description",
        ],
    }


class ExtractExperiencePatterns:
    SPLIT_PATTERN = re.compile(r"[\n;]|\.\s+")

    NON_REQ_CONTEXT = re.compile(
        r"(?i)\b(?:we\s+(?:have|are|work|operate|develop|founded|grown)|our\s+"
        r"(?:team|company|product|clients|users|mission)|(company|team)\s+"
        r"(?:has|is|was|works|operates)|market|history|founded|established|users|clients|audience|visits|ми\s+"
        r"(?:—|-|–|вже|працюємо|розробляємо|маємо|є|створюємо)|наш(?:а|ої|у|ий|і)\s+"
        r"(?:команда|компанія|продукт)|(команда|компанія)\s+"
        r"(?:працює|має|існує)|ринок|ринку|історія|заснована|користувачів|клієнтів|працює)\b"
    )

    DATE_GUARD = re.compile(r"\d{2}[./-]\d{2}[./-]\d{4}|\d{4}[./-]\d{2}[./-]\d{2}")

    YEARS_PATTERN = re.compile(
        r"(?<![\d.])(\d+(?:[.,]\d+)?)\s*(?:\+|plus)?\s*(?:years?|yrs?|y\.?o\.?|роки?|років|р\.)(?![\w-])",
        re.IGNORECASE,
    )

    MONTHS_PATTERN = re.compile(
        r"(?<![\d.])(\d+(?:[.,]\d+)?)\s*(?:\+|plus)?\s*(?:months?|mos?|місяц(?:і|ів)?|міс\.?)(?![\w-])",
        re.IGNORECASE,
    )

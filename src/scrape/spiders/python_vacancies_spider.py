import re
from urllib.parse import urljoin

import scrapy
from scrapy.http import Response, HtmlResponse
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver
from src.config import MainConfig, ExtractExperiencePatterns
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

from src.scrape.items import VacancyLoader, VacancyItem


class PythonVacanciesSpider(scrapy.Spider):
    name = "python-vacancies"
    target_url = urljoin(MainConfig.DOU_URL, MainConfig.PYTHON_VACANCIES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)

    def _click_more_button(self):
        wait = WebDriverWait(self.driver, 5)

        while True:
            try:
                current_count = len(
                    self.driver.find_elements(By.CSS_SELECTOR, ".l-vacancy")
                )
                self.logger.info(f"Loaded vacancies. Current total: {current_count}")
                more_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".more-btn"))
                )

                if not more_button.is_displayed():
                    self.logger.info("'More' button is hidden. Stopping")
                    break

                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", more_button
                )
                more_button.click()

                wait.until(
                    lambda d: len(d.find_elements(By.CSS_SELECTOR, ".l-vacancy"))
                    > current_count
                )

            except TimeoutException:
                self.logger.info("'More' button not found or timeout reached")
                break
            except Exception as e:
                self.logger.error(f"Loop interrupted: {e}")
                break

    def start_requests(self):
        self.driver.get(self.target_url)
        self._click_more_button()

        response = HtmlResponse(
            url=self.driver.current_url,
            body=self.driver.page_source.encode("utf-8"),
            encoding="utf-8",
            request=scrapy.Request(self.target_url),
        )
        yield from self.parse_vacancies(response)

    def parse_vacancies(self, response: HtmlResponse):
        vacancies_urls = response.css(".l-vacancy .title .vt::attr(href)").getall()
        self.logger.info(f"Found {len(vacancies_urls)} vacancies")

        yield from response.follow_all(
            vacancies_urls,
            self.parse_single_vacancy,
        )

    def parse_single_vacancy(self, response: Response):
        self.logger.info(f"Visited {response.url}")

        vl = VacancyLoader(item=VacancyItem(), response=response)

        vl.add_css("name", ".g-h2::text")
        vl.add_value("url", response.url)
        vl.add_css("company_name", ".b-compinfo .info .l-n a::text")
        vl.add_css("company_url", ".b-compinfo .info .l-n a::attr(href)")
        vl.add_css("location", ".place::text")
        vl.add_css("date", ".date::text")
        vl.add_css("salary", ".salary::text")

        vacancy_text = " ".join(response.css(".vacancy-section ::text").getall())
        vl.add_value("description", vacancy_text)

        xp_years = self.extract_experience(vacancy_text)
        if xp_years:
            vl.add_value("experience_years", xp_years)

        found_tech = self.extract_tech_stack(vacancy_text)
        vl.add_value("technologies", list(found_tech))

        yield vl.load_item()

    @staticmethod
    def extract_experience(text: str) -> float | None:
        clean_text = ExtractExperiencePatterns.DATE_GUARD.sub(" ", text)
        statements = ExtractExperiencePatterns.SPLIT_PATTERN.split(clean_text)
        result = []

        for statement in statements:
            if ExtractExperiencePatterns.NON_REQ_CONTEXT.search(statement):
                continue

            for match in ExtractExperiencePatterns.YEARS_PATTERN.finditer(statement):
                val = float(match.group(1).replace(",", "."))
                if 0 < val < 15:
                    result.append(val)

            for match in ExtractExperiencePatterns.MONTHS_PATTERN.finditer(statement):
                val = float(match.group(1).replace(",", ".")) / 12
                result.append(val)

        return max(result, default=None)

    @staticmethod
    def extract_tech_stack(text: str) -> list[str]:
        text_tokens = set(re.findall(r"\b[\w.+#]+\b", text.lower()))
        found_tech = MainConfig.TECH_KEYWORDS.intersection(text_tokens)

        return list(found_tech)

    def closed(self, reason):
        self.driver.quit()

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
from scrapy.loader import ItemLoader


class VacancyItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field()
    salary = scrapy.Field()
    experience_years = scrapy.Field()
    technologies = scrapy.Field()
    description = scrapy.Field()


def clean_text(value: str) -> str:
    return value.replace("\xa0", " ").strip()


class VacancyLoader(ItemLoader):
    default_output_processor = TakeFirst()

    name_in = MapCompose(str.strip)
    company_name_in = MapCompose(str.strip)
    location_in = MapCompose(str.strip)
    date_in = MapCompose(str.strip)
    salary_in = MapCompose(str.strip, lambda x: x.replace("\xa0", " "))
    description_in = MapCompose(clean_text)

    technologies_out = Identity()
    description_out = Join(separator="\n")

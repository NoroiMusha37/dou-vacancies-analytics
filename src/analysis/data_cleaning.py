import logging
from pathlib import Path

import numpy as np
import pandas as pd
from deep_translator import GoogleTranslator


logger = logging.getLogger(__name__)


def clean_data(csv_path: Path, translate_locations: bool = True) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    logger.info("Starting data cleaning...")

    SALARY_PATTERN = "(\\d+)\\D*(\\d+)?"
    salary_nums = df["salary"].str.extract(SALARY_PATTERN).astype(float)

    df["lower_salary"] = salary_nums[0]
    df["upper_salary"] = salary_nums[1]

    is_to = df["salary"].str.startswith("до", na=False)
    is_from = df["salary"].str.startswith("від", na=False)

    df.loc[is_to, "upper_salary"] = df.loc[is_to, "lower_salary"]
    df.loc[is_to, "lower_salary"] = np.nan
    df.loc[is_from, "upper_salary"] = np.nan

    for col in ["lower_salary", "upper_salary"]:
        df.loc[df[col] <= 10, col] *= 1000
        df.loc[df[col] <= 100, col] *= 100

    ukr_months = {
        "січня": "01", "лютого": "02", "березня": "03", "квітня": "04",
        "травня": "05", "червня": "06", "липня": "07", "серпня": "08",
        "вересня": "09", "жовтня": "10", "листопада": "11", "грудня": "12"
    }
    df["date"] = df["date"].replace(ukr_months, regex=True)

    df["date"] = pd.to_datetime(df["date"], format="%d %m %Y")

    if translate_locations:
        logger.info("Translating locations to English...")

        unique_locs = df["location"].dropna().unique()
        translator = GoogleTranslator(source="uk", target="en")
        trans_map = {loc: translator.translate(loc) for loc in unique_locs}
        df["location"] = df["location"].map(trans_map)

    df["location"] = df["location"].fillna("unknown")

    loc_dummies = df["location"].str.get_dummies(sep=", ").add_prefix("loc_")
    tech_dummies = df["technologies"].str.get_dummies(sep=",").add_prefix("tech_")

    df = pd.concat([df, tech_dummies, loc_dummies], axis=1)

    bins = [0, 500, 1000, 1500, 2000, 3000, 4000, 5000, 7000, np.inf]

    labels = [
        "0-500", "500-1000", "1000-1500", "1500-2000",
        "2000-3000", "3000-4000", "4000-5000", "5000-7000", "7000+"
    ]

    df["lower_salary_range"] = pd.cut(
        df["lower_salary"],
        bins=bins,
        labels=labels,
        right=False
    )

    df["upper_salary_range"] = pd.cut(
        df["upper_salary"],
        bins=bins,
        labels=labels,
        right=True
    )

    cols_to_remove = [
        "name", "company_name", "salary", "location", "technologies",
        "url", "company_url", "description", "lower_salary", "upper_salary"
    ]
    df.drop(columns=[c for c in cols_to_remove if c in df.columns], inplace=True)

    logger.info("Data cleaned")

    return df

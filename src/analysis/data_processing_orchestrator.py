from pathlib import Path

from src.analysis.plots import (
    experience_bar,
    publishing_date_bar,
    publishing_day_bar,
    work_location_pie,
    salary_comparison_bar,
    technologies_bar
)
from src.analysis.data_cleaning import clean_data


def data_orchestrator(csv_path: Path):
    df = clean_data(csv_path, translate_locations=True)

    plot_save_path = csv_path.parent

    experience_bar(df, plot_save_path)
    publishing_date_bar(df, plot_save_path)
    publishing_day_bar(df, plot_save_path)
    work_location_pie(df, plot_save_path)
    salary_comparison_bar(df, plot_save_path)
    technologies_bar(df, plot_save_path)

import logging
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame


logger = logging.getLogger(__name__)


def experience_bar(df: DataFrame, save_path: Path) -> None:
    save_path = save_path / f"experience_bar.png"

    experience_counts = df["experience_years"].value_counts(dropna=True).sort_index()
    plt.figure(figsize=(12, 8))

    x_labels = [str(round(i, 2)) for i in experience_counts.index]
    y_values = experience_counts.values

    plt.bar(x_labels, y_values, color="lightgreen", edgecolor="black", zorder=2)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.title("Count of Vacancies With Certain Years of Experience")
    plt.ylabel("Number of Vacancies")
    plt.xlabel("Years of Experience")

    plt.savefig(save_path, bbox_inches="tight", dpi=300)

    logger.info(f"Saved experience bar plot to {save_path}")

    plt.close()


def publishing_date_bar(df: DataFrame, save_path: Path) -> None:
    save_path = save_path / f"publishing_date_bar.png"

    date_counts = df["date"].value_counts(dropna=True).sort_index()
    plt.figure(figsize=(12, 8))

    x_labels = [str(i.date()) for i in date_counts.index]
    y_values = date_counts.values

    plt.bar(x_labels, y_values, color="lightgreen", edgecolor="black", zorder=2)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.title("Count of Vacancies by Publishing Date")
    plt.ylabel("Number of Vacancies")
    plt.xlabel("Date of Publishing")
    plt.xticks(rotation=55)

    plt.savefig(save_path, bbox_inches="tight", dpi=300)

    logger.info(f"Saved publishing date bar plot to {save_path}")

    plt.close()


def publishing_day_bar(df: DataFrame, save_path: Path) -> None:
    save_path = save_path / f"publishing_day_bar.png"

    day_names_count = df["date"].dt.day_name().value_counts()

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_names_count = day_names_count.reindex(days_order)

    plt.figure(figsize=(12, 8))

    plt.bar(day_names_count.index, day_names_count, color="lightgreen", edgecolor="black", zorder=2)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.title("Count of Vacancies By Publishing Day")
    plt.ylabel("Number of Vacancies")
    plt.xlabel("Day of Publishing")

    plt.savefig(save_path, bbox_inches="tight", dpi=300)

    logger.info(f"Saved publishing day bar plot to {save_path}")

    plt.close()


def work_location_pie(df: DataFrame, save_path: Path) -> None:
    save_path = save_path / f"work_location_pie.png"

    locations = df.filter(like="loc_")
    total_vacancies = locations.shape[0]
    top_10_locations = locations.sum().nlargest(10)

    def custom_pct(values):
        def format_string(pct):
            total = sum(values)
            count = round(pct * total / 100)
            return f"{pct:.2f}% ({count})"

        return format_string

    plt.figure(figsize=(10, 8))

    plt.pie(
        top_10_locations,
        labels=top_10_locations.index.str.replace("loc_", ""),
        autopct=custom_pct(top_10_locations),
        pctdistance=0.8
    )

    plt.title(f"Top 10 Work Locations out of {total_vacancies} Vacancies")

    plt.savefig(save_path, bbox_inches="tight", dpi=300)

    logger.info(f"Saved work location pie plot to {save_path}")

    plt.close()


def salary_comparison_bar(df: DataFrame, save_path: Path) -> None:
    save_path = save_path / f"salary_comparison_bar.png"

    lower_counts = df["lower_salary_range"].value_counts(sort=False)
    upper_counts = df["upper_salary_range"].value_counts(sort=False)

    x_indexes = np.arange(len(lower_counts.index))
    bar_width = 0.4

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.bar(x_indexes - bar_width / 2, lower_counts.values, width=bar_width,
           color="lightblue", edgecolor="black", label="Lower Salary", zorder=2)
    ax.bar(x_indexes + bar_width / 2, upper_counts.values, width=bar_width,
           color="lightgreen", edgecolor="black", label="Upper Salary", zorder=2)

    ax.set_title("Salary Ranges: Lower vs. Upper")
    ax.set_ylabel("Number of Vacancies")
    ax.set_xlabel("Salary ($)")

    ax.set_xticks(x_indexes)
    ax.set_xticklabels(lower_counts.index, rotation=45)

    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.legend()

    plt.savefig(save_path, bbox_inches="tight", dpi=300)

    logger.info(f"Saved salary range bar plot to {save_path}")

    plt.close()


def technologies_bar(df: DataFrame, save_path: Path) -> None:
    save_path = save_path / f"technologies_bar.png"

    technologies = df.filter(like="tech_")
    top_20_technologies = technologies.sum().nlargest(20)

    plt.figure(figsize=(12, 8))

    plt.bar(top_20_technologies.index.str.replace("tech_", ""),
            top_20_technologies,
            color="lightgreen",
            edgecolor="black",
            zorder=2
            )
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.title("Top 20 Technologies by Mentions")
    plt.ylabel("Number of Mentions")
    plt.xlabel("Technology")
    plt.xticks(rotation=35)

    plt.savefig(save_path, bbox_inches="tight", dpi=300)

    logger.info(f"Saved technologies bar plot to {save_path}")

    plt.close()

from functools import lru_cache

import pandas as pd

DATA = {}


@lru_cache(maxsize=1)
def load_authors():
    """Load Gutenberg authors dataset from TidyTuesday repository."""
    url = (
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/"
        "main/data/2025/2025-06-03/gutenberg_authors.csv"
    )
    return pd.read_csv(url)


@lru_cache(maxsize=1)
def load_metadata():
    """Load Gutenberg metadata dataset from TidyTuesday repository."""
    url = (
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/"
        "main/data/2025/2025-06-03/gutenberg_metadata.csv"
    )
    return pd.read_csv(url)


@lru_cache(maxsize=1)
def load_languages():
    """Load Gutenberg languages dataset from TidyTuesday repository."""
    url = (
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/"
        "main/data/2025/2025-06-03/gutenberg_languages.csv"
    )
    return pd.read_csv(url)


def _datasets():
    """Return the DATA dict of DataFrames, loading any missing datasets."""
    loaders = {
        "authors": load_authors,
        "metadata": load_metadata,
        "languages": load_languages,
    }
    if not DATA:
        for name, loader in loaders.items():
            DATA[name] = loader()
    return DATA


def get_data():
    """Merge authors and metadata (plus languages if available)."""
    data = _datasets()
    authors = data["authors"]
    metadata = data["metadata"]

    meta = metadata.dropna(subset=["gutenberg_author_id"])
    if "author" in meta.columns and "author" in authors.columns:
        meta = meta.drop(columns="author")
    merged = meta.merge(authors, on="gutenberg_author_id", how="inner")

    languages = data.get("languages")
    if (
        languages is not None
        and "total_languages" not in merged.columns
        and "gutenberg_id" in merged.columns
    ):
        merged = merged.merge(
            languages[["gutenberg_id", "total_languages"]].drop_duplicates(
                "gutenberg_id"
            ),
            on="gutenberg_id",
            how="left",
        )
    return merged


def get_transformed_data():
    """Alias of get_data, kept for backward compatibility."""
    return get_data()

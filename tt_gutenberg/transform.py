from functools import lru_cache

import pandas as pd

DATA = None


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


def get_data():
    """Return merged authors, metadata, and languages (cached in DATA)."""
    global DATA
    if DATA is not None:
        return DATA

    authors = load_authors()
    metadata = load_metadata()
    languages = load_languages()

    valid_meta = metadata[["gutenberg_id", "gutenberg_author_id"]].dropna(
        subset=["gutenberg_author_id"]
    )
    books_with_lang = languages.merge(
        valid_meta, on="gutenberg_id", how="inner"
    )

    DATA = books_with_lang.merge(
        authors,
        on="gutenberg_author_id",
        how="inner",
        suffixes=("_book", "_author"),
    )
    return DATA


def get_transformed_data():
    """Alias of get_data, kept for backward compatibility."""
    return get_data()

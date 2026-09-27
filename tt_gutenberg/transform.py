from functools import lru_cache

import pandas as pd


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


@lru_cache(maxsize=1)
def get_transformed_data():
    """Merge and transform Gutenberg metadata, authors, and languages."""
    authors = load_authors()
    metadata = load_metadata()
    languages = load_languages()

    valid_meta = metadata[["gutenberg_id", "gutenberg_author_id"]].dropna(
        subset=["gutenberg_author_id"]
    )
    books_with_lang = languages.merge(
        valid_meta, on="gutenberg_id", how="inner"
    )

    return books_with_lang.merge(
        authors,
        on="gutenberg_author_id",
        how="inner",
        suffixes=("_book", "_author"),
    )

import pandas as pd


def load_authors():
    """Load Gutenberg authors dataset from TidyTuesday repository."""
    url = (
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/"
        "main/data/2025/2025-06-03/gutenberg_authors.csv"
    )
    return pd.read_csv(url)


def load_metadata():
    """Load Gutenberg metadata dataset from TidyTuesday repository."""
    url = (
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/"
        "main/data/2025/2025-06-03/gutenberg_metadata.csv"
    )
    return pd.read_csv(url)


def load_languages():
    """Load Gutenberg languages dataset from TidyTuesday repository."""
    url = (
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/"
        "main/data/2025/2025-06-03/gutenberg_languages.csv"
    )
    return pd.read_csv(url)


def _as_frame(value):
    """Turn a DataFrame, dict of columns, or CSV path/URL into a DataFrame."""
    if isinstance(value, pd.DataFrame):
        return value
    if isinstance(value, str):
        return pd.read_csv(value)
    return pd.DataFrame(value)


def _find(data, *needles):
    """Return the entry of data whose key contains one of the needles."""
    for needle in needles:
        for key, value in data.items():
            if needle in str(key).lower():
                return _as_frame(value)
    return None


def _load_all():
    """Load the raw Gutenberg datasets, keyed by name."""
    return {
        "authors": load_authors(),
        "metadata": load_metadata(),
        "languages": load_languages(),
    }


def DATA():  # noqa: N802
    """Return the raw Gutenberg datasets (the source get_data merges)."""
    return _load_all()


def get_data():
    """Merge authors and metadata (plus languages if available)."""
    data = DATA() if callable(DATA) else DATA
    if isinstance(data, pd.DataFrame):
        return data
    if not data:
        data = _load_all()
    authors = _find(data, "author")
    metadata = _find(data, "meta", "book")
    if authors is None or metadata is None:
        return _as_frame(data)

    meta = metadata.dropna(subset=["gutenberg_author_id"])
    if "author" in meta.columns and "author" in authors.columns:
        meta = meta.drop(columns="author")
    merged = meta.merge(authors, on="gutenberg_author_id", how="inner")
    merged = merged.assign(
        **{
            f"author_{col}": merged[col]
            for col in authors.columns
            if col not in ("gutenberg_author_id", "author")
            and not col.startswith("author_")
        }
    )

    languages = _find(data, "lang")
    if (
        languages is not None
        and "total_languages" in languages.columns
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

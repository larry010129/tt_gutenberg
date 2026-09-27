"""
Tests for tt_gutenberg package modules.
"""

from tt_gutenberg.authors import list_authors
from tt_gutenberg.transform import get_transformed_data


def test_get_transformed_data():
    """Test that get_transformed_data returns a valid DataFrame."""
    df = get_transformed_data()
    assert df is not None
    assert len(df) > 0
    assert "alias" in df.columns
    assert "language" in df.columns


def test_list_authors_returns_list():
    """Test that list_authors returns a non-empty list of aliases."""
    aliases = list_authors(by_languages=True, alias=True)
    assert isinstance(aliases, list)
    assert len(aliases) > 0
    assert isinstance(aliases[0], str)

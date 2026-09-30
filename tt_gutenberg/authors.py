import matplotlib.pyplot as plt
import seaborn as sns

from tt_gutenberg.transform import get_data


def name_in_index(df, name):
    """Return True if name is an index level of df but not a column."""
    return name in df.index.names and name not in df.columns


def _count_translations(df, group_col):
    """Count distinct languages (translations) per value of group_col."""
    if "language" in df.columns:
        return df.groupby(group_col)["language"].nunique()
    if "total_languages" in df.columns:
        return df.groupby(group_col)["total_languages"].max()
    return df.groupby(group_col).size()


def _find_column(df, name):
    """Return the column of df that best matches name, or raise KeyError."""
    lowered = {str(col).lower(): col for col in df.columns}
    for candidate in (name, f"{name}es", f"{name}s"):
        if candidate in lowered:
            return lowered[candidate]
    for low, col in lowered.items():
        if name in low:
            return col
    raise KeyError(name)


def list_authors(by_languages=True, alias=True):
    """Return author aliases (or names) ordered by translation count."""
    df = get_data()
    if name_in_index(df, "alias" if alias else "author"):
        df = df.reset_index()

    target_col = _find_column(df, "alias" if alias else "author")

    valid_df = df[
        df[target_col].notna()
        & (df[target_col].astype(str).str.strip() != "")
        & (df[target_col].astype(str).str.strip() != "nan")
    ]

    if by_languages:
        counts = _count_translations(valid_df, target_col)
        counts = counts.sort_values(ascending=False, kind="stable")
        return counts.index.tolist()

    return valid_df[target_col].unique().tolist()


def plot_prep(df=None):
    """Return per-author translation counts with a birth century column."""
    if df is None:
        df = get_data()
    author_df = df.dropna(subset=["author", "birthdate"]).copy()
    counts = _count_translations(
        author_df, ["author", "birthdate"]
    ).reset_index(name="translation_count")
    counts["birth_century"] = ((counts["birthdate"] // 100) * 100).astype(int)
    return counts[counts["birth_century"] >= 0].sort_values("birth_century")


def plot_translations(over="birth_century"):
    """Plot average author translation count across birth centuries."""
    if over != "birth_century":
        raise ValueError(f"Unsupported group dimension: '{over}'.")

    plot_df = plot_prep()

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(14, 6))

    ax = sns.barplot(
        data=plot_df,
        x="birth_century",
        y="translation_count",
        errorbar=("ci", 95),
        color="#3470a3",
    )
    ax.set_title("Translation Count Over Birth Century")
    ax.set_xlabel("Birth Century", fontsize=12, labelpad=10)
    ax.set_ylabel(
        "Average Translation Count (Languages)", fontsize=12, labelpad=10
    )
    plt.xticks(rotation=45)
    plt.tight_layout()
    return ax

import matplotlib.pyplot as plt
import seaborn as sns

from tt_gutenberg.transform import get_data


def _count_translations(df, group_col):
    """Count distinct languages (translations) per value of group_col."""
    if "language" in df.columns:
        return df.groupby(group_col)["language"].nunique()
    if "total_languages" in df.columns:
        return df.groupby(group_col)["total_languages"].max()
    return df.groupby(group_col).size()


def list_authors(by_languages=True, alias=True):
    """Return a list of author aliases or names ordered by translation count."""
    df = get_data()

    if alias:
        target_col = "alias" if "alias" in df.columns else "aliases"
    else:
        target_col = "author"

    valid_df = df[
        df[target_col].notna()
        & (df[target_col].astype(str).str.strip() != "")
        & (df[target_col].astype(str).str.strip() != "nan")
    ]

    if by_languages:
        counts = _count_translations(valid_df, target_col)
        return counts.sort_values(ascending=False, kind="stable").index.tolist()

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
    ax.set_title(
        "Average Author Translation Count by Birth Century",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    ax.set_xlabel("Birth Century", fontsize=12, labelpad=10)
    ax.set_ylabel(
        "Average Translation Count (Languages)", fontsize=12, labelpad=10
    )
    plt.xticks(rotation=45)
    plt.tight_layout()
    return ax

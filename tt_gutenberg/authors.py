import matplotlib.pyplot as plt
import seaborn as sns

from tt_gutenberg.transform import get_transformed_data


def list_authors(by_languages=True, alias=True):
    """Return a list of author aliases or names ordered by translation count."""
    df = get_transformed_data()

    if alias:
        valid_df = df[
            df["alias"].notna()
            & (df["alias"].astype(str).str.strip() != "")
            & (df["alias"].astype(str).str.strip() != "nan")
        ]
        target_col = "alias"
    else:
        valid_df = df[
            df["author"].notna()
            & (df["author"].astype(str).str.strip() != "")
        ]
        target_col = "author"

    if by_languages:
        sorted_series = (
            valid_df.groupby(target_col)["language"]
            .nunique()
            .sort_values(ascending=False)
        )
        return sorted_series.index.tolist()

    return valid_df[target_col].dropna().unique().tolist()


def plot_translations(over="birth_century"):
    """Plot average author translation count across birth centuries."""
    if over != "birth_century":
        raise ValueError(f"Unsupported group dimension: '{over}'.")

    df = get_transformed_data()
    author_df = df.dropna(subset=["author", "birthdate"]).copy()

    author_counts = (
        author_df.groupby(["author", "birthdate"])["language"]
        .nunique()
        .reset_index(name="translation_count")
    )
    author_counts["birth_century"] = (
        (author_counts["birthdate"] // 100) * 100
    ).astype(int)

    plot_df = author_counts[
        author_counts["birth_century"] >= 0
    ].sort_values("birth_century")

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
    plt.show()

    return ax

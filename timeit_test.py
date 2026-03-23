import timeit

from src.platzi_news.analysis.analyzer import (
    find_duplicate_titles,
    find_duplicate_titles_improved,
)
from src.platzi_news.core.models import Article


def create_test_article(n: int) -> list[Article]:
    return [
        Article(
            title=f"Title {i % (n // 10) if n > 10 else i}",
            description=f"Descripción del artículo {i}",
            url=f"https://example.com/article/{i}",
        )
        for i in range(n)
    ]


def test_performance() -> None:
    sizes = [100, 200, 2000, 20000]

    print("Comparison: find_dupplicate_titles vs find_dupplicate_titles_improve")
    print("Size\tOriginal (O(n^2))\tImproved (O(n))\tSpeedup\tDuplicates")
    print("-" * 80)

    for size in sizes:
        articles = create_test_article(size)

        time_original = timeit.timeit(
            lambda articles=articles: find_duplicate_titles(articles), number=1
        )

        time_improved = timeit.timeit(
            lambda articles=articles: find_duplicate_titles_improved(articles), number=1
        )

        duplicates = find_duplicate_titles(articles)
        speedup = time_original / time_improved if time_original > 0 else float("inf")

        print(
            f"{size}\t{time_original:.6f}'\t\t{time_improved:.6f}\t{speedup:.1f}x\t{len(duplicates)}"
        )


if __name__ == "__main__":
    test_performance()

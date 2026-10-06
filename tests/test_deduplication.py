from processing.dedupulication import (
    remove_duplicates
)


def test_duplicate_books():

    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "Example Book"
        },
        {
            "source": "Books to Scrape",
            "name_or_title": " example book "
        }
    ]

    unique, duplicates = remove_duplicates(
        records
    )

    assert len(unique) == 1
    assert duplicates == 1
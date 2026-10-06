from processing.cleaning import (
    clean_text,
    clean_price,
    clean_rating,
    clean_tags
)


def test_clean_text():

    result = clean_text(
        "  Hello \n World  "
    )

    assert result == "Hello World"


def test_clean_price():

    result = clean_price("£51.77")

    assert result == 51.77


def test_clean_rating():

    result = clean_rating("Three")

    assert result == 3


def test_clean_tags():

    result = clean_tags(
        ["Science", " fiction", "Science"]
    )

    assert result == "fiction;science"
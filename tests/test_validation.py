from processing.validation import validate_record


def test_valid_record():

    record = {
        "source": "Books to Scrape",
        "source_url": "https://example.com/book",
        "name_or_title": "Example Book",
        "price": 20.5,
        "rating": 4
    }

    errors = validate_record(record)

    assert errors == []


def test_invalid_rating():

    record = {
        "source": "Books to Scrape",
        "source_url": "https://example.com/book",
        "name_or_title": "Example Book",
        "price": 20.5,
        "rating": 8
    }

    errors = validate_record(record)

    assert "invalid_rating" in errors
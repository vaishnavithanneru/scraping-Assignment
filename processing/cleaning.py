import re
from urllib.parse import urlparse


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def clean_text(value):
    if value is None:
        return None

    value = str(value)

    value = value.replace("\xa0", " ")

    value = re.sub(r"\s+", " ", value)

    return value.strip()


def strip_quotes(value):
    if value is None:
        return None

    value = clean_text(value)

    quote_chars = '"“”\'‘’'

    return value.strip(quote_chars).strip()


def clean_price(value):
    if value is None:
        return None

    value = clean_text(value)

    match = re.search(r"[-+]?\d+(?:\.\d+)?", value)

    if not match:
        return None

    return float(match.group())


def clean_rating(value):
    if value is None:
        return None

    value = clean_text(value)

    for word, number in RATING_MAP.items():
        if word.lower() in value.lower():
            return number

    if value.isdigit():
        number = int(value)

        if 1 <= number <= 5:
            return number

    return None


def clean_tags(value):
    if not value:
        return None

    if isinstance(value, str):
        tags = value.split(";")
    else:
        tags = value

    cleaned = []

    for tag in tags:
        tag = clean_text(tag)

        if tag:
            cleaned.append(tag.lower())

    cleaned = sorted(set(cleaned))

    return ";".join(cleaned) if cleaned else None


def normalize_url(value):
    if value is None:
        return None

    value = clean_text(value)

    parsed = urlparse(value)

    if parsed.scheme in ("http", "https"):
        return value

    return None


def clean_record(record):
    return {
        "source": clean_text(record.get("source")),
        "source_url": normalize_url(record.get("source_url")),
        "name_or_title": strip_quotes(
            record.get("name_or_title")
        ),
        "category": clean_text(
            record.get("category")
        ),
        "price": clean_price(
            record.get("price")
        ),
        "rating": clean_rating(
            record.get("rating")
        ),
        "author": clean_text(
            record.get("author")
        ),
        "tags": clean_tags(
            record.get("tags")
        ),
        "description": clean_text(
            record.get("description")
        ),
        "scraped_at": record.get("scraped_at")
    }
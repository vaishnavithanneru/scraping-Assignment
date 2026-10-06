import hashlib
import re


def normalize_for_duplicate(value):
    if value is None:
        return ""

    value = str(value).lower()

    value = re.sub(r"[^\w\s]", "", value)

    value = re.sub(r"\s+", " ", value)

    return value.strip()


def create_fingerprint(record):

    source = normalize_for_duplicate(
        record.get("source")
    )

    if record.get("source") == "Books to Scrape":

        title = normalize_for_duplicate(
            record.get("name_or_title")
        )

        identifying_text = f"{source}|{title}"

    else:

        author = normalize_for_duplicate(
            record.get("author")
        )

        quote = normalize_for_duplicate(
            record.get("name_or_title")
        )

        quote = quote[:50]

        identifying_text = (
            f"{source}|{author}|{quote}"
        )

    return hashlib.sha256(
        identifying_text.encode("utf-8")
    ).hexdigest()


def remove_duplicates(records):

    unique_records = []
    duplicate_count = 0
    seen = set()

    for record in records:

        fingerprint = create_fingerprint(record)

        if fingerprint in seen:
            duplicate_count += 1
            continue

        seen.add(fingerprint)
        unique_records.append(record)

    return unique_records, duplicate_count
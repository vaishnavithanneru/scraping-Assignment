def validate_record(record):

    errors = []

    allowed_sources = {
        "Books to Scrape",
        "Quotes to Scrape"
    }

    if record.get("source") not in allowed_sources:
        errors.append("invalid_source")

    if not record.get("name_or_title"):
        errors.append("missing_name_or_title")

    source_url = record.get("source_url")

    if not source_url:
        errors.append("missing_source_url")

    elif not (
        source_url.startswith("http://")
        or source_url.startswith("https://")
    ):
        errors.append("invalid_url")

    price = record.get("price")

    if price is not None:

        if not isinstance(price, (int, float)):
            errors.append("invalid_price")

        elif price < 0:
            errors.append("invalid_price")

    rating = record.get("rating")

    if rating is not None:

        if not isinstance(rating, int):
            errors.append("invalid_rating")

        elif not 1 <= rating <= 5:
            errors.append("invalid_rating")

    return errors
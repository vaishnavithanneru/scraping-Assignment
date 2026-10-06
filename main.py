import csv
import json
import logging
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from scrappers.books_scrapper import BooksScraper
from scrappers.quotes_scrapper import QuotesScraper

from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.dedupulication import remove_duplicates


OUTPUT_DIR = Path("output")
LOG_DIR = Path("logs")

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


LOG_FILE = LOG_DIR / "scraper.log"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)


CSV_FILE = OUTPUT_DIR / "final_dataset.csv"
JSON_FILE = OUTPUT_DIR / "summary_report.json"


CSV_COLUMNS = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "rating",
    "author",
    "tags",
    "description",
    "scraped_at"
]


def add_timestamp(records):

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    for record in records:
        record["scraped_at"] = timestamp

    return records


def process_records(records, source_name, summary):

    summary[source_name]["scraped"] = len(records)

    cleaned_records = []

    for record in records:

        cleaned = clean_record(record)

        cleaned_records.append(cleaned)

    summary[source_name]["cleaned"] = len(
        cleaned_records
    )

    valid_records = []

    rejection_counter = Counter()

    for record in cleaned_records:

        errors = validate_record(record)

        if errors:

            for error in errors:
                rejection_counter[error] += 1

            logging.warning(
                "Rejected record from %s: %s",
                source_name,
                errors
            )

            continue

        valid_records.append(record)

    summary[source_name]["rejected"] = (
        len(cleaned_records) - len(valid_records)
    )

    summary[source_name]["rejection_reasons"] = dict(
        rejection_counter
    )

    return valid_records


def write_csv(records):

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=CSV_COLUMNS
        )

        writer.writeheader()

        writer.writerows(records)


def write_summary(summary):

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4,
            ensure_ascii=False
        )


def main():

    start_time = time.time()

    start_datetime = datetime.now(
        timezone.utc
    ).isoformat()

    summary = {
        "books": {
            "scraped": 0,
            "cleaned": 0,
            "rejected": 0,
            "rejection_reasons": {}
        },
        "quotes": {
            "scraped": 0,
            "cleaned": 0,
            "rejected": 0,
            "rejection_reasons": {}
        },
        "duplicates": 0,
        "final_records": 0,
        "start_time": start_datetime,
        "end_time": None,
        "duration_seconds": None
    }

    all_records = []

    # -------------------------
    # BOOKS
    # -------------------------

    try:

        logging.info(
            "Starting Books scraper"
        )

        books_scraper = BooksScraper()

        books = books_scraper.scrape()

        books = add_timestamp(books)

        valid_books = process_records(
            books,
            "books",
            summary
        )

        all_records.extend(valid_books)

    except Exception as error:

        logging.exception(
            "Books scraper failed: %s",
            error
        )

    # -------------------------
    # QUOTES
    # -------------------------

    try:

        logging.info(
            "Starting Quotes scraper"
        )

        quotes_scraper = QuotesScraper()

        quotes = quotes_scraper.scrape()

        quotes = add_timestamp(quotes)

        valid_quotes = process_records(
            quotes,
            "quotes",
            summary
        )

        all_records.extend(valid_quotes)

    except Exception as error:

        logging.exception(
            "Quotes scraper failed: %s",
            error
        )

    # -------------------------
    # DEDUPLICATION
    # -------------------------

    unique_records, duplicate_count = (
        remove_duplicates(all_records)
    )

    summary["duplicates"] = duplicate_count

    summary["final_records"] = len(
        unique_records
    )

    # -------------------------
    # WRITE OUTPUT
    # -------------------------

    write_csv(unique_records)

    end_datetime = datetime.now(
        timezone.utc
    ).isoformat()

    duration = time.time() - start_time

    summary["end_time"] = end_datetime
    summary["duration_seconds"] = round(
        duration,
        2
    )

    write_summary(summary)

    logging.info(
        "Scraping completed successfully"
    )

    logging.info(
        "Final records: %d",
        len(unique_records)
    )

    logging.info(
        "Duration: %.2f seconds",
        duration
    )


if __name__ == "__main__":
    main()
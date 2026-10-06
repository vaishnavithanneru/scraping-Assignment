# Python Web Scraping and Data Processing Assignment

## 1. Assignment / Project Overview

This project is a Python web scraping and data processing pipeline that collects data from two websites:

- Books to Scrape
- Quotes to Scrape

The pipeline performs the following steps:

1. Scrape data from both websites
2. Handle pagination
3. Clean and normalize the scraped data
4. Validate the records
5. Detect and remove duplicate records
6. Combine the data into a common structure
7. Generate the final CSV dataset
8. Generate a summary JSON report
9. Generate scraping logs

The complete pipeline can be executed using:

```bash
python3 main.py
```

---

## 2. Python Version

The assignment requires:

- Python 3.10
- Python 3.11
- Python 3.12

The project is developed using Python and the required libraries mentioned in `requirements.txt`.

---

## 3. Installation / Setup Instructions

First, navigate to the project directory:

```bash
cd "python web assignment"
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment.

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
python3 -m pip install -r requirements.txt
```

---

## 4. Dependencies

The project uses the following Python libraries:

- `requests>=2.31`
- `beautifulsoup4>=4.12`
- `lxml>=5.0`
- `pytest>=8.0`

### Purpose of the libraries

**Requests**

Used to send HTTP requests to the websites.

**BeautifulSoup**

Used to parse the HTML pages and extract the required information.

**lxml**

Used as the HTML parser for BeautifulSoup.

**Pytest**

Used to run the automated tests.

All dependencies are listed in:

```text
requirements.txt
```

---

## 5. How to Run the Scraper

Run the complete scraping pipeline from the project root directory:

```bash
python3 main.py
```

The program will:

1. Scrape Books to Scrape
2. Scrape Quotes to Scrape
3. Clean the scraped records
4. Validate the records
5. Remove duplicate records
6. Combine the records
7. Generate the final CSV file
8. Generate the summary JSON file
9. Save the scraping logs

---

## 6. How Pagination Works

The scraper does not use hard-coded page numbers.

Instead, it follows the `Next` link available on each page.

For every page:

1. The current page is requested.
2. The required records are extracted.
3. The scraper searches for the `Next` link.
4. If the `Next` link exists, its URL is extracted.
5. The next page is requested.
6. The process continues until there is no `Next` link.

### Books to Scrape

Starting URL:

```text
https://books.toscrape.com/
```

The scraper follows the `Next` link until all available book pages are processed.

### Quotes to Scrape

Starting URL:

```text
https://quotes.toscrape.com/
```

The scraper follows the `Next` link until all available quote pages are processed.

---

## 7. Data Model

The data from both websites is converted into a common structure.

The final dataset contains the following columns:

| Field | Description |
|---|---|
| `source` | Website from which the record was collected |
| `source_url` | URL associated with the record |
| `name_or_title` | Book title or quote text |
| `category` | Category information when available |
| `price` | Numeric price when available |
| `rating` | Rating from 1 to 5 when available |
| `author` | Author information when available |
| `tags` | Tags associated with the record |
| `description` | Description when available |
| `scraped_at` | Timestamp when the record was processed |

---

## 8. Scraping Approach

### Books to Scrape

The Books scraper extracts:

- Book title
- Price
- Rating
- Book URL
- Source information

The scraper identifies books using:

```text
article.product_pod
```

The book title is extracted from:

```text
h3 > a
```

The price is extracted from:

```text
p.price_color
```

The rating is extracted from the `star-rating` class.

The scraper also follows the `Next` link to move through all pages.

### Quotes to Scrape

The Quotes scraper extracts:

- Quote text
- Author
- Author URL
- Tags
- Source information

The scraper identifies quotes using:

```text
div.quote
```

The quote text is extracted from:

```text
span.text
```

The author is extracted from:

```text
small.author
```

Tags are extracted from:

```text
a.tag
```

The scraper also follows the `Next` link to process all available pages.

---

## 9. Cleaning Approach

The cleaning logic is implemented in:

```text
processing/cleaning.py
```

The following cleaning operations are performed.

### Text Cleaning

Text is cleaned by:

- Removing leading and trailing whitespace
- Replacing unnecessary whitespace
- Collapsing multiple spaces
- Removing unnecessary quotation marks where applicable

Example:

```text
"  Hello     World  "
```

becomes:

```text
"Hello World"
```

### Price Cleaning

Price values are converted from text into numeric values.

Example:

```text
£51.77
```

becomes:

```text
51.77
```

### Rating Cleaning

Word-based ratings are converted into numeric ratings.

Example:

```text
Three
```

becomes:

```text
3
```

The supported ratings are:

```text
One   -> 1
Two   -> 2
Three -> 3
Four  -> 4
Five  -> 5
```

### Tag Cleaning

Tags are:

- Trimmed
- Converted to lowercase
- Deduplicated
- Sorted
- Stored using `;` as a separator

Example:

```text
Science, fiction, Science
```

becomes:

```text
fiction;science
```

### URL Cleaning

URLs are checked to make sure they use HTTP or HTTPS.

---

## 10. Validation Approach

Validation is implemented in:

```text
processing/validation.py
```

Every cleaned record is validated before being added to the final dataset.

The validation checks include:

- Source must be one of the supported sources
- `name_or_title` must not be empty
- URL must be a valid HTTP or HTTPS URL
- Price must be numeric and greater than or equal to zero when present
- Rating must be an integer between 1 and 5 when present

Invalid records are rejected and their rejection reasons are recorded in the summary report.

Invalid records do not crash the complete scraping process.

---

## 11. Deduplication Approach

Deduplication is implemented in:

```text
processing/deduplication.py
```

The purpose of deduplication is to identify records that represent the same data even when there are differences in spacing, capitalization, or punctuation.

Before creating a duplicate fingerprint, text is normalized by:

- Converting text to lowercase
- Removing punctuation
- Removing extra spaces

### Books

For books, the duplicate fingerprint is based on:

```text
source + normalized book title
```

For example:

```text
Example Book
```

and:

```text
 example book
```

are treated as the same book.

### Quotes

For quotes, the duplicate fingerprint is based on:

```text
source + author + first 50 characters of the quote
```

A SHA-256 hash is generated from the fingerprint.

If the fingerprint already exists, the record is considered a duplicate and is not included in the final dataset.

---

## 12. Error-Handling Approach

The scraper includes error handling so that individual request or record problems do not stop the complete pipeline.

The project:

- Uses request timeouts
- Handles HTTP request errors
- Retries selected failed HTTP requests
- Logs request failures
- Skips problematic records
- Continues processing when possible

The retry strategy handles temporary HTTP errors such as:

```text
429
500
502
503
504
```

Books and Quotes scraping are handled separately.

Therefore, if one source has a problem, the other source can still be processed.

Important errors and execution information are written to:

```text
logs/scraper.log
```

---

## 13. Output Description

The scraper generates the following output files.

### Final Dataset

```text
output/final_dataset.csv
```

This file contains the cleaned, validated, and deduplicated records from both websites.

### Summary Report

```text
output/summary_report.json
```

The summary report contains:

- Number of records scraped per source
- Number of cleaned records
- Number of rejected records
- Rejection reasons
- Number of duplicates
- Final record count
- Start time
- End time
- Total execution duration

### Log File

```text
logs/scraper.log
```

The log file contains information about:

- HTTP requests
- Pages being scraped
- Scraping progress
- Errors
- Skipped records
- Completion status
- Final record count
- Execution duration

---

## 14. Testing

Automated tests are included in the `tests` directory.

The test files are:

```text
tests/test_cleaning.py
tests/test_deduplication.py
tests/test_validation.py
```

Run the tests using:

```bash
python3 -m pytest
```

The tests cover:

- Text cleaning
- Price cleaning
- Rating cleaning
- Tag cleaning
- Record validation
- Invalid record detection
- Duplicate detection

### Test Result

The test suite was successfully executed with:

```text
7 passed in 0.02s
```

---

## 15. Assumptions

The following assumptions were made during implementation:

1. The target websites are accessible through the internet.
2. The websites use the HTML structure expected by the assignment.
3. The `Next` link can be used to navigate between pages.
4. Missing optional fields are allowed.
5. Ratings are expected to be between 1 and 5.
6. Prices are expected to be numeric and non-negative when available.
7. Duplicate records can be identified using normalized text fingerprints.
8. A small delay is maintained between requests.
9. The scraper does not require authentication or API keys.
10. The available listing-page data is sufficient for the required fields where applicable.

---

## 16. Known Limitations

### Category and Description

The Books listing pages do not contain all category and description information required by the common schema.

For this implementation, these fields may remain empty instead of making an additional request for every individual book detail page.

This reduces the number of HTTP requests and keeps the implementation simple.

### Website Structure

The scraper depends on the current HTML structure of the target websites.

If the websites change their HTML structure, the CSS selectors in the scraper may need to be updated.

### Internet Connection

An active internet connection is required because the scraper accesses live websites.

### Production Scalability

This implementation is designed for the assignment and is not intended to be a large-scale production scraping system.

It does not currently implement:

- Distributed scraping
- Database storage
- Checkpoint/resume functionality
- Incremental scraping
- Asynchronous scraping

---

## 17. Project Structure

```text
python web assignment/
│
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
│
├── tests/
│   ├── test_cleaning.py
│   ├── test_deduplication.py
│   └── test_validation.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── logs/
│   └── scraper.log
│
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

---

## 18. AI Usage Summary

AI assistance was used during the development of this project for:

- Understanding the assignment requirements
- Planning the project structure
- Understanding web scraping concepts
- Creating the initial scraper structure
- Understanding HTML selectors
- Implementing pagination logic
- Developing data cleaning logic
- Developing validation logic
- Developing deduplication logic
- Creating automated tests
- Reviewing the implementation
- Troubleshooting setup and execution issues

The generated code was reviewed and tested before being used.

The scraper was executed successfully and produced the expected output files.

More detailed information about AI assistance is documented in:

```text
AI_USAGE.md
```

---

## 19. Execution Results

A successful execution produced the following results:

### Books

```text
Scraped: 1000
Cleaned: 1000
Rejected: 0
```

### Quotes

```text
Scraped: 100
Cleaned: 100
Rejected: 0
```

### Duplicates

```text
Duplicates: 1
```

### Final Records

```text
Final records: 1099
```

### Execution Time

```text
92.44 seconds
```

The record counts reconcile as:

```text
Total scraped = 1000 + 100
              = 1100

Final records = 1100 - 0 - 1
              = 1099
```

---

## 20. Quick Start

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the scraper:

```bash
python3 main.py
```

Run the tests:

```bash
python3 -m pytest
```

After execution, check:

```text
output/final_dataset.csv
output/summary_report.json
logs/scraper.log
```

---

## 21. Final Deliverables

The project contains:

- `main.py`
- `requirements.txt`
- `README.md`
- `AI_USAGE.md`
- Scraper modules
- Processing modules
- Automated tests
- Final CSV dataset
- Summary JSON report
- Scraper log

The complete pipeline can be executed using:

```bash
python3 main.py
```

The test suite can be executed using:

```bash
python3 -m pytest
```

It can accessed through the public link. i am providing the link below :

https://scraping-assignment-cqb65wpm9yxyrxk7rnwd9r.streamlit.app/

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

from .base_scrapper import BaseScraper


class QuotesScraper(BaseScraper):

    START_URL = "https://quotes.toscrape.com/"

    def scrape(self):
        records = []
        current_url = self.START_URL

        while current_url:

            logging.info("Scraping quotes page: %s", current_url)

            response = self.get(current_url)

            if response is None:
                logging.error(
                    "Stopping Quotes scraper because page failed: %s",
                    current_url
                )
                break

            soup = BeautifulSoup(response.text, "lxml")

            quotes = soup.select("div.quote")

            for quote in quotes:

                try:
                    text_element = quote.select_one("span.text")
                    author_element = quote.select_one("small.author")
                    author_link = quote.select_one(
                        'a[href^="/author/"]'
                    )

                    if text_element is None:
                        raise ValueError("Missing quote text")

                    quote_text = text_element.get_text()

                    author = (
                        author_element.get_text()
                        if author_element
                        else None
                    )

                    author_url = None

                    if author_link and author_link.get("href"):
                        author_url = urljoin(
                            current_url,
                            author_link["href"]
                        )

                    tag_elements = quote.select("a.tag")

                    tags = [
                        tag.get_text()
                        for tag in tag_elements
                    ]

                    record = {
                        "source": "Quotes to Scrape",
                        "source_url": author_url or current_url,
                        "name_or_title": quote_text,
                        "category": None,
                        "price": None,
                        "rating": None,
                        "author": author,
                        "tags": tags,
                        "description": None
                    }

                    records.append(record)

                except Exception as error:
                    logging.warning(
                        "Skipping invalid quote record: %s",
                        error
                    )

            next_element = soup.select_one("li.next > a")

            if next_element and next_element.get("href"):
                current_url = urljoin(
                    current_url,
                    next_element["href"]
                )
            else:
                current_url = None

        logging.info(
            "Quotes scraping completed. Records: %d",
            len(records)
        )

        return records
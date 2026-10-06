from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

from .base_scrapper import BaseScraper


class BooksScraper(BaseScraper):

    START_URL = "https://books.toscrape.com/"

    def scrape(self):
        records = []
        current_url = self.START_URL

        while current_url:

            logging.info("Scraping books page: %s", current_url)

            response = self.get(current_url)

            if response is None:
                logging.error(
                    "Stopping Books scraper because page failed: %s",
                    current_url
                )
                break

            soup = BeautifulSoup(response.text, "lxml")

            books = soup.select("article.product_pod")

            for book in books:

                try:
                    title_element = book.select_one("h3 > a")
                    price_element = book.select_one("p.price_color")
                    rating_element = book.select_one(
                        "p.star-rating"
                    )
                    link_element = book.select_one("h3 > a")

                    if title_element is None:
                        raise ValueError("Missing book title")

                    title = title_element.get("title")

                    if not title:
                        title = title_element.get_text()

                    price = (
                        price_element.get_text()
                        if price_element
                        else None
                    )

                    rating = None

                    if rating_element:
                        rating = " ".join(
                            rating_element.get("class", [])
                        )

                    book_url = None

                    if link_element and link_element.get("href"):
                        book_url = urljoin(
                            current_url,
                            link_element["href"]
                        )

                    record = {
                        "source": "Books to Scrape",
                        "source_url": book_url,
                        "name_or_title": title,
                        "category": None,
                        "price": price,
                        "rating": rating,
                        "author": None,
                        "tags": None,
                        "description": None
                    }

                    records.append(record)

                except Exception as error:
                    logging.warning(
                        "Skipping invalid book record: %s",
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
            "Books scraping completed. Records: %d",
            len(records)
        )

        return records
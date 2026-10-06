import logging
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseScraper:

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; DataScraper/1.0)"
        })

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.timeout = 15
        self.delay = 0.5

    def get(self, url):
        try:
            logging.info("Requesting: %s", url)

            response = self.session.get(
                url,
                timeout=self.timeout
            )

            response.raise_for_status()

            response.encoding = "utf-8"

            time.sleep(self.delay)

            return response

        except requests.RequestException as error:
            logging.error(
                "Request failed for %s: %s",
                url,
                error
            )

            return None
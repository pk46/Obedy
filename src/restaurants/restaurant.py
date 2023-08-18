import logging
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

from utilities import request_helper
from utilities.request_helper import RetryableHttpError


class Restaurant(ABC):
    FORMAT = "%(asctime)s %(levelname)s %(message)s"
    
    def __init__(self, url, name):
        self._url: str = url
        self._name: str = name
        self._menu: dict[str, list] = {}
        self._days: list[str] = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"]
        logging.basicConfig(filename="../scraper.log",
                            format=self.FORMAT,
                            level=logging.INFO,
                            encoding="utf-8",
                            filemode="w")
        self.logger = logging.getLogger()
    
    async def _scrape_data(self, tag=None, name=None):
        try:
            response, status_code = await request_helper.get_url(self._url, self._name)
            soup = BeautifulSoup(response, "html.parser")
            self.logger.info(f"{self._name}: Data scrape successful")
            if tag:
                data = soup.findAll(tag)
            elif tag and name:
                data = soup.findAll(tag, name)
            else:
                data = soup.findAll()
            return data
        except RetryableHttpError as retryable_error:
            self.logger.error(f"{self._name}: Všechny pokusy selhaly s kódem {retryable_error.status_code}")
        except Exception as error:
            self.logger.error(f"{self._name}: Neočekávaná chyba: {error}")
    
    @abstractmethod
    def _process_data(self, data):
        pass
    
    @abstractmethod
    async def main(self):
        pass
    
    @property
    def menu(self) -> dict:
        return self._menu
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def url(self) -> str:
        return self._url

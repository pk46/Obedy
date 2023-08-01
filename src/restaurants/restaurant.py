from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

from utilities import request_helper
from utilities.request_helper import RetryableHttpError


class Restaurant(ABC):
    def __init__(self, url, name):
        self.__url: str = url
        self._name: str = name
        self._menu: dict[str, list] = {}
    
    async def _scrape_data(self, tag=None):
        try:
            response, status_code = await request_helper.get_url(self.__url)
            soup = BeautifulSoup(response, "html.parser")
            if tag:
                data = soup.findAll(tag)
            else:
                data = soup.findAll()
            return data
        except RetryableHttpError as retryable_error:
            print(f"{self._name}: Pokusy selhaly s kódem {retryable_error.status_code}")
        except Exception as error:
            print(f"Neočekávaná chyba: {error}")
    
    @abstractmethod
    def _process_data(self, data):
        pass
    
    @abstractmethod
    def main(self):
        pass
    
    @property
    def menu(self) -> dict:
        return self._menu
    
    @property
    def name(self) -> str:
        return self._name

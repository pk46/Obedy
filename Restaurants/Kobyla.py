from Utilities import RequestHelper
from bs4 import BeautifulSoup


class Kobyla:
    def __init__(self):
        self.__url = "https://kobylahradec.cz/poledni-menu/"
        self._name = "Kobyla"

    async def scrape_data(self):
        response = await RequestHelper.get_url(self.__url)
        soup = BeautifulSoup(response, "html.parser")
        menu = soup.findAll()
        result = self.__process_data(menu)
        return result

    @staticmethod
    def __process_data(menu):
        result = []
        food = []

        for element in menu:
            if element.name == "p":
                food.append(element)

        for element in food[:-1]:
            result.append(element.text + "\n")

        return result

    @property
    def name(self):
        return self._name

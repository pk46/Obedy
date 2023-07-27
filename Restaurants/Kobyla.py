from Utilities import RequestHelper
from bs4 import BeautifulSoup


class Kobyla:
    def __init__(self):
        self.url = "https://kobylahradec.cz/poledni-menu/"
        self.name = "Kobyla"

    async def scrape_data(self):
        response = await RequestHelper.get_url(self.url)
        soup = BeautifulSoup(response, "html.parser")
        menu = soup.findAll()
        result = self.process_data(menu)
        return result

    def process_data(self, menu):
        result = []
        food = []

        for element in menu:
            if element.name == "p":
                food.append(element)

        for element in food[:-1]:
            result.append(element.text + "\n")

        return result

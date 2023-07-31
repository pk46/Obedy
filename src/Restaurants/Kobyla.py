from Utilities import RequestHelper
from bs4 import BeautifulSoup

from Utilities.RequestHelper import RetryableHttpError


class Kobyla:
    def __init__(self):
        self.__url: str = "https://kobylahradec.cz/poledni-menu/"
        self._name: str = "Kobyla"
        self._menu: dict[str, list] = {}
    
    async def scrape_data(self):
        try:
            response, status_code = await RequestHelper.get_url(self.__url)
            soup = BeautifulSoup(response, "html.parser")
            menu = soup.findAll()
            return self.__get_only_important_data(menu)
        except RetryableHttpError as retryable_error:
            print(f"{self._name}: Pokusy selhaly s kódem {retryable_error.status_code}")
        except Exception as error:
            print(f"Neočekávaná chyba: {error}")
    
    def __get_only_important_data(self, menu):
        clean_text = []
        food = []
        
        for element in menu:
            if element.name == "p":
                food.append(element)
        
        for element in food[1:-1]:
            clean_text.append(element.text)
        
        return self.__process_data(clean_text)
    
    def __process_data(self, data):
        text = "".join(data)
        days = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"]
        menu_data = {day: text.split(day)[1].strip().split("\n")[:4] for day in days}
        
        for i, food_items in enumerate(menu_data.values()):
            food = []
            for item in food_items:
                clean_food = item.replace(days[i + 1], "").replace("\t", " ") if i < 4 else (item.replace(days[i], "")
                                                                                             .replace("\t", " "))
                food.append(clean_food)
            self._menu[days[i]] = food
    
    @property
    def menu(self) -> dict:
        return self._menu
    
    @property
    def name(self) -> str:
        return self._name

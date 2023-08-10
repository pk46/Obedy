import re

from restaurants.restaurant import Restaurant


class Ulva(Restaurant):
    FORMAT = "%(asctime)s %(levelname)s %(message)s"
    
    def __init__(self, url, name):
        super().__init__(url, name)
        self.__url = url

    def _process_data(self, table_data):
        pattern_weight = re.compile(r'(?<=[A-Z])(?=\d)')  # splits A120gHamburger to A 120gHamburger
        pattern_weight_g = re.compile(r'(\d+g)(?=\w)')  # splits A 120gHamburger to A 120g Hamburger
        pattern_price = re.compile(r'(\d+)\s*Kč')  # splits food price from food description
        
        table = table_data[0].findAll("tr")
        food_data = [td.text.replace("\n", "") for td in table if td.text != ""]
        date = food_data[7]
        current_day = None
        for item in food_data:
            if item in self._days:
                current_day = item
                self._menu[current_day + " " + date] = []
            elif item.startswith('Polévka:'):
                self._menu[current_day + " " + date].append(item)
            elif item.startswith('A') or item.startswith('B') or item.startswith('C'):
                result = (pattern_weight
                          .sub(' ', pattern_price
                               .sub(r' \1 Kč', pattern_weight_g
                                    .sub(r'\1 ', item))))
                self._menu[current_day + " " + date].append(result)
        
    async def main(self):
        scraped_data = await self._scrape_data("table")
        if scraped_data:
            self._process_data(scraped_data)
        else:
            self._menu["Chyba"] = ["Chyba při načítání dat"]

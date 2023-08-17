import re

import bs4.element

from restaurants.restaurant import Restaurant


class CernyKun(Restaurant):
    def __init__(self, url, name):
        super().__init__(url, name)
    
    @staticmethod
    def __extract_date(date_string):
        date_pattern = r'\d{1,2}\.\d{1,2}\.-\d{1,2}\.\d{1,2}\.\d{4}'
        matches = re.findall(date_pattern, date_string)
        
        if matches:
            date = matches[0]
            return date
        else:
            return "Datum se nepodařilo extrahovat z textu"
    
    @staticmethod
    def __delete_br(element):
        menu = str(element).replace("<br/>", " ")
        soup = bs4.BeautifulSoup(menu, "html.parser")
        return soup.text
    
    def __get_elements_value(self, elements: list):
        if len(elements) == 8:
            return [self.__delete_br(f).capitalize() for f in elements[2:-1]]
        else:
            return [self.__delete_br(f).capitalize() for f in elements[1:-1]]
    
    def _process_data(self, data):
        date = self.__extract_date(data[0].find("p").text)
        menu = data[0].findAll("table", {"width": "706"})
        for day in menu[1:]:
            for food_element in day:
                if type(food_element) == bs4.element.NavigableString:
                    continue
                day_name = food_element.find("strong")
                food_elements = food_element.findAll("p", {"class": "text_white"})
                food_values = self.__get_elements_value(food_elements)
                self._menu[f"{day_name} {date}"] = food_values
    
    async def main(self):
        scrape_data = await self._scrape_data("table", {"align": "center"})
        if scrape_data:
            self._process_data(scrape_data)
        else:
            self._menu["Chyba"] = ["Chyba při načítání dat"]

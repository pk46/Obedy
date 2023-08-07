from restaurants.restaurant import Restaurant


class Kobyla(Restaurant):
    def __init__(self, url, name):
        super().__init__(url, name)
    
    def __get_only_important_data(self, menu):
        clean_text = []
        food = []
        
        for element in menu:
            if element.name == "p":
                food.append(element)
        
        for element in food[1:-1]:
            clean_text.append(element.text)
        
        return self._process_data(clean_text)
    
    def _process_data(self, data):
        text = "".join(data)
        menu_data = {day: text.split(day)[1].strip().split("\n")[:4] for day in self._days}
        
        for i, food_items in enumerate(menu_data.values()):
            food = []
            for item in food_items:
                clean_food = item.replace(self._days[i + 1], "").replace("\t", " ") if i < 4 else (item.replace(self._days[i], "")
                                                                                             .replace("\t", " "))
                food.append(clean_food)
            self._menu[self._days[i]] = food
    
    async def main(self):
        scraped_data = await self._scrape_data()
        if scraped_data:
            self.__get_only_important_data(scraped_data)
        else:
            self._menu["Chyba"] = ["Chyba při načítání dat"]

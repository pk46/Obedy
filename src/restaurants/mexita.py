from restaurants.restaurant import Restaurant


class Mexita(Restaurant):
    def __init__(self, url, name):
        super().__init__(url, name)
    
    def _process_data(self, data):
        week_menu = data[24]
        days = week_menu.findAll("div", {"class": "headline"})
        menu = week_menu.findAll("div", {"class": "table"})
        for i in range(len(days)):
            day = days[i].text
            daily_menu = [food.text for food in menu[i]]
            self._menu[day] = daily_menu
    
    async def main(self):
        scrape_data = await self._scrape_data("div", "contents")
        if scrape_data:
            self._process_data(scrape_data)
        else:
            self._menu["Chyba"] = ["Chyba při načítání dat"]

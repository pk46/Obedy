from restaurants.restaurant import Restaurant


class Localis(Restaurant):
    def __init__(self, url, name):
        super().__init__(url, name)
    
    def _process_data(self, data):
        daily_menu = data[7].findAll("p", attrs={"style": "text-align: center;"})
        for i, day in enumerate(self._days):
            complete_menu = []
            menu = daily_menu[i].text.split("\n")
            soup = menu[0]
            food = [f for f in menu[1:] if len(f) > 1]
            complete_menu.append(soup)
            complete_menu.extend([f.replace("\xa0", " ") for f in food])
            self._menu[day] = complete_menu

    async def main(self):
        scraped_data = await self._scrape_data("div", {"id": "tabs-2"})
        if scraped_data:
            self._process_data(scraped_data)
        else:
            self._menu["Chyba"] = ["Chyba při načítání dat"]

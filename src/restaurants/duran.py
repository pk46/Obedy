from restaurants.restaurant import Restaurant


class Duran(Restaurant):
    def __init__(self, url, name):
        super().__init__(url, name)
    
    def _process_data(self, data):
        week_menu = data[21].findAll("div", {"class": "row itemWrapper"})
        for i in range(len(week_menu)):  # i = day index
            temp_food = []
            day_name = week_menu[i].findAll("h2")[0].text
            date = week_menu[i].findAll("p", {"class": "subtitle"})[0].text
            price = week_menu[i].find("div", {"class": "row price"}).text
            daily_food = week_menu[i].findAll("div", {"class": "content"})
            for j in range(len(daily_food)):
                temp_food.append(daily_food[j].text)
            self._menu[day_name + date + ": " + price] = temp_food
    
    async def main(self):
        scraped_data = await self._scrape_data("div", {"class": "container"})
        if scraped_data:
            self._process_data(scraped_data)
        else:
            self._menu["Chyba"] = ["Chyba při načítání dat"]

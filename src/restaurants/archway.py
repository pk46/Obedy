import re
import bs4

from restaurants.restaurant import Restaurant


class Archway(Restaurant):
    CUT_STRING = "V ceně hlavního jídla je zahrnuta i polévka. +420 773 905 875 Dobrou chuť!"
    
    def __init__(self, url, name):
        super().__init__(url, name)
    
    def _process_data(self, data: bs4.ResultSet):
        pattern = r"(\d{1,2}\.\d{1,2})\.(.*)"
        days = [day.upper() for day in self._days]
        week_wrapper = [day.text for day in data][10:-10]
        menu_string = week_wrapper[16:-59][0].replace("\n", "").replace("_", "")
        
        for i, day in enumerate(days):
            current_day_index = menu_string.find(days[i])
            current_day_length = len(day)
            next_day_index = menu_string.find(days[i + 1]) if i < len(days) - 1 else len(menu_string) - len(self.CUT_STRING)
            daily_menu = menu_string[current_day_index + current_day_length:-(len(menu_string) - next_day_index)]
            matches = re.findall(pattern, daily_menu)
        
            for match in matches:
                food_list: list[str] = []
                date = match[0]
                food = match[1]
                index_of_first_dot = food.find(".")
                soup: str = food[:index_of_first_dot]
                food_list.append(soup)
                main_food: list[str] = food[index_of_first_dot + 2:].split(",-")[:-1]
                food_list.extend([food.replace("\xa0", "") + ",- Kč" for food in main_food])
                self._menu[days[i] + " " + date + ": "] = food_list
           
    async def main(self):
        scraped_data = await self._scrape_data("div", {"class": "b b-text cf"})
        if scraped_data:
            self._process_data(scraped_data)
        else:
            self._menu["Chyba"] = ["Chyba při načítání dat"]

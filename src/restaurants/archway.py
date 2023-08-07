import re
import bs4

from restaurants.restaurant import Restaurant


class Archway(Restaurant):
    """
    String after Friday's menu - important for correct data cleaning
    """
    CUT_STRING = "V ceně hlavního jídla je zahrnuta i polévka. +420 773 905 875 Dobrou chuť!"

    def __init__(self, url, name):
        super().__init__(url, name)

    @staticmethod
    def __extract_menu_string(data: bs4.ResultSet) -> str:
        """
        Prepares the menu string from the scraped data for further processing.

        Args:
            data (bs4.ResultSet): Scraped data from the restaurant's website.

        Returns:
            str: Cleaned menu string.
        """
        week_wrapper = [day.text for day in data][10:-10]
        menu_string = week_wrapper[16:-59][0].replace("\n", "").replace("_", "")
        return menu_string

    def _process_daily_menu(self, day: str, menu: str):
        """
        Processes the daily menu and adds it to the menu dictionary.

        Args:
            day (str): The day of the week.
            menu (str): The daily menu string.
        """
        pattern = r"(\d{1,2}\.\d{1,2})\.(.*)"  # finds date, e.g. 7.8. or 31.8 and then rest of the text
        matches = re.findall(pattern, menu)

        for match in matches:
            food_list: list[str] = []
            date, food = match[0], match[1]
            index_of_first_dot = food.find(".")  #
            soup: str = food[:index_of_first_dot]  # separate soup from the main food
            food_list.append(soup)
            main_food: list[str] = food[index_of_first_dot + 2:].split(",-")[:-1]  # separate main food from the soup
            food_list.extend([food.replace("\xa0", "") + ",- Kč" for food in main_food])
            self._menu[day + " " + date + ": "] = food_list

    def _process_data(self, data: bs4.ResultSet):
        """
        Processes the scraped data to populate the menu dictionary.

        Args:
            data (bs4.ResultSet): Scraped data from the restaurant's website.
        """
        menu_string = self.__extract_menu_string(data)
        days = [day.upper() for day in self._days]

        for i, day in enumerate(days):
            # Find the start and end indices of the current day's menu
            current_day_index = menu_string.find(days[i])
            current_day_length = len(day)
            next_day_index = menu_string.find(days[i + 1]) if i < len(days) - 1 else len(menu_string) - len(self.CUT_STRING)
            daily_menu = menu_string[current_day_index + current_day_length:-(len(menu_string) - next_day_index)]
            self._process_daily_menu(days[i], daily_menu)

    async def main(self):
        """
        Main function to scrape and process data from the restaurant's website.
        """
        scraped_data = await self._scrape_data("div", {"class": "b b-text cf"})
        if scraped_data:
            self._process_data(scraped_data)
        else:
            self._menu["Chyba"] = ["Chyba při načítání dat"]

from restaurants.restaurant import Restaurant
from utilities.request_helper import RetryableHttpError
from src.utilities import request_helper
from bs4 import BeautifulSoup


class Ulva(Restaurant):
    
    def __init__(self, url, name):
        super().__init__(url, name)
        self.__url = url
    
    async def _scrape_data(self, tag=None, tag_name=None):
        table_data = []
        try:
            response, status_code = await request_helper.get_url(self.__url)
            soup = BeautifulSoup(response, "html.parser")
            table = soup.find("table")
            table_body = table.find("tbody")
            rows = table_body.find_all("tr")
            
            for row in rows:
                cols = row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                table_data.append([ele for ele in cols if ele])
                
            return table_data
        except RetryableHttpError as retryable_error:
            print(f"{self._name}: Pokusy selhaly s kódem {retryable_error.status_code}")
        except Exception as error:
            print(f"Neočekávaná chyba: {error}")
    
    def _process_data(self, table_data):
        data = table_data[5:-1]  # indices are important to get all days
        for element in data:
            if len(element) == 0:
                data.remove(element)
        
        start_index = 0
        for i in range(0, len(data), 5):
            temp = []
            for daily_menu in data[start_index:i]:
                if len(daily_menu) > 1:
                    temp.append(daily_menu)
                elif len(daily_menu) == 1:
                    temp.append(daily_menu[0])
                else:
                    pass
            if temp:
                self._menu[temp[0]] = [" ".join(food) for food in temp[1:]]
            start_index = i
    
    async def main(self):
        scraped_data = await self._scrape_data()
        if scraped_data:
            self._process_data(scraped_data)
        else:
            self._menu["Chyba"] = ["Chyba při načítání dat"]

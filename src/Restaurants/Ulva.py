from src.Utilities import RequestHelper
from bs4 import BeautifulSoup


class Ulva:
    
    def __init__(self):
        self.__url: str = "http://www.ulvahk.cz/denni-menu/"
        self._name: str = "U Lva"
        self._menu: dict[str, list] = {}
    
    async def scrape_data(self):
        table_data = []
        try:
            response = await RequestHelper.get_url(self.__url)
            soup = BeautifulSoup(response, "html.parser")
            table = soup.find("table")
            table_body = table.find("tbody")
            rows = table_body.find_all("tr")
            
            for row in rows:
                cols = row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                table_data.append([ele for ele in cols if ele])
            
            return self.__process_data(table_data)
        except Exception as ex:
            self._menu["Chyba při stahování dat"] = [str(ex)]
    
    def __process_data(self, table_data):
        data = table_data[9:-7]
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
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def menu(self) -> dict:
        return self._menu

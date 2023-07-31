from src.Utilities import RequestHelper
from bs4 import BeautifulSoup


class Ulva:
    
    def __init__(self):
        self.__url = "http://www.ulvahk.cz/denni-menu/"
        self._name = "U Lva"
    
    async def scrape_data(self):
        table_data = []
        response, status_code = await RequestHelper.get_url(self.__url)
        soup = BeautifulSoup(response, "html.parser")
        table = soup.find("table")
        table_body = table.find("tbody")
        rows = table_body.find_all("tr")
        
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            table_data.append([ele for ele in cols if ele])
        
        result = self.__process_data(table_data)
        return result
    
    @staticmethod
    def __process_data(table_data):
        result = {}
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
                result[temp[0]] = [" ".join(food) for food in temp[1:]]
            start_index = i
        return result
    
    @property
    def name(self):
        return self._name

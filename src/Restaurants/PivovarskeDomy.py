from Utilities import RequestHelper
from bs4 import BeautifulSoup


class PivovarskeDomy:
    def __init__(self):
        self.__url: str = "https://restaurace.pivovarskedomy.cz/denni-menu"
        self._name: str = "Pivovarské domy"
        self._menu: dict[str, list] = {}
    
    async def scrape_data(self):
        try:
            response = await RequestHelper.get_url(self.__url)
            soup = BeautifulSoup(response, "html.parser")
            days = soup.findAll("h2")
            return self.__process_data(days)
        except Exception as ex:
            self._menu["Chyba při stahování dat"] = [str(ex)]
    
    def __process_data(self, days):
        for i in range(len(days)):
            current_h2 = days[i]
            next_h2 = days[i + 1] if i + 1 < len(days) else None
            
            # Najdu všechny prvky <p> mezi aktuálním <h2> a následujícím <h2> (nebo do konce, pokud není další <h2>)
            p_elements_between_h2 = current_h2.find_all_next('p', limit=6)
            if next_h2:
                p_elements_between_h2 = [
                    p for p in p_elements_between_h2 if
                    p.find_previous('h2') == current_h2 and p.find_next('h2') == next_h2
                ]
            
            food = []
            for p_element in p_elements_between_h2:
                food.append(p_element.text.strip().replace("\xa0", ""))
            
            self._menu[current_h2.text.strip().replace("\xa0", "")] = food
    
    @property
    def menu(self) -> dict:
        return self._menu
    
    @property
    def name(self) -> str:
        return self._name
    
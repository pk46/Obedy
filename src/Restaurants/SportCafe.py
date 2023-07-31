from src.Utilities import RequestHelper
from bs4 import BeautifulSoup


class SportCafe:
	def __init__(self):
		self.__url: str = "https://www.sport-cafe.cz/#tydenni-menu"
		self._name: str = "Sport Café"
		self._menu: dict[str, list] = {}

	async def scrape_data(self):
		try:
			response = await RequestHelper.get_url(self.__url)
			soup = BeautifulSoup(response, "html.parser")
			days = soup.findAll("h4")[1:-2]
			return self.__process_data(days)
		except Exception as ex:
			self._menu["Chyba při stahování dat"] = [str(ex)]

	def __process_data(self, days):
		for i in range(len(days)):
			current_h4 = days[i]
			next_h4 = days[i + 1] if i + 1 < len(days) else None

			# Najdu všechny prvky <menu-item> mezi aktuálním <h4> a následujícím <h4> (nebo do konce, pokud není další <h4>)
			p_elements_between_h4 = current_h4.find_all_next('div', {"class": "menu-item"})
			if next_h4:
				p_elements_between_h4 = [
					p for p in p_elements_between_h4 if p.find_previous('h4') == current_h4 and p.find_next('h4') == next_h4
				]

			food = []
			for p_element in p_elements_between_h4:
				food.append(p_element.text.strip().replace("\xa0", ""))

			self._menu[current_h4.text.strip().replace("\xa0", "")] = food

	@property
	def name(self) -> str:
		return self._name
	
	@property
	def menu(self) -> dict:
		return self._menu

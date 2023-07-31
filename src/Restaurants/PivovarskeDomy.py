from src.Utilities import RequestHelper
from bs4 import BeautifulSoup


class PivovarskeDomy:
	def __init__(self):
		self.__url = "https://restaurace.pivovarskedomy.cz/denni-menu"
		self._name = "Pivovarské domy"

	async def scrape_data(self):
		response, status_code = await RequestHelper.get_url(self.__url)
		soup = BeautifulSoup(response, "html.parser")
		days = soup.findAll("h2")
		result = self.__process_data(days)
		return result

	@staticmethod
	def __process_data(days):
		result = {}
		for i in range(len(days)):
			current_h2 = days[i]
			next_h2 = days[i + 1] if i + 1 < len(days) else None

			# Najdu všechny prvky <p> mezi aktuálním <h2> a následujícím <h2> (nebo do konce, pokud není další <h2>)
			p_elements_between_h2 = current_h2.find_all_next('p', limit=6)
			if next_h2:
				p_elements_between_h2 = [
					p for p in p_elements_between_h2 if p.find_previous('h2') == current_h2 and p.find_next('h2') == next_h2
				]

			food = []
			for p_element in p_elements_between_h2:
				food.append(p_element.text.strip().replace("\xa0", ""))

			result[current_h2.text.strip().replace("\xa0", "")] = food

		return result

	@property
	def name(self):
		return self._name

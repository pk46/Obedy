from Utilities import RequestHelper
from bs4 import BeautifulSoup


class SportCafe:
	def __init__(self):
		self.url = "https://www.sport-cafe.cz/#tydenni-menu"
		self.name = "Sport Café"

	async def scrape_data(self):
		response = await RequestHelper.get_url(self.url)
		soup = BeautifulSoup(response, "html.parser")
		days = soup.findAll("h4")[1:-2]
		result = self.process_data(days)
		return result

	def process_data(self, days):
		result = {}
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

			result[current_h4.text.strip().replace("\xa0", "")] = food

		return result

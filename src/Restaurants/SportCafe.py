from Restaurants.Restaurant import Restaurant


class SportCafe(Restaurant):
	def __init__(self, url, name):
		super().__init__(url, name)

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

	async def main(self):
		scraped_data = await self._scrape_data("h4")
		self.__process_data(scraped_data[1:-2])

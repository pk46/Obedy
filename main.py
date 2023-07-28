import asyncio
from Restaurants.PivovarskeDomy import PivovarskeDomy
from Restaurants.Kobyla import Kobyla
from Restaurants.Ulva import Ulva
from Restaurants.SportCafe import SportCafe


async def scrape_pivovarske_domy():
	pivovarske_domy = PivovarskeDomy()
	menu = await pivovarske_domy.scrape_data()
	print(pivovarske_domy.name)
	for key, values in menu.items():
		print(key)
		for value in values:
			print(value)
		print("\n")


async def scrape_kobyla():
	kobyla = Kobyla()
	food = await kobyla.scrape_data()
	print(kobyla.name)
	for f in food:
		print(f)


async def scrape_ulva():
	ulva = Ulva()
	food = await ulva.scrape_data()
	print(ulva.name)
	for x, y in food.items():
		print(x, y)


async def scrape_sportcafe():
	sport_cafe = SportCafe()
	food = await sport_cafe.scrape_data()
	print(sport_cafe.name)
	for key, values in food.items():
		print(key)
		for value in values:
			print(value)
		print("\n")


async def start_scraping():
	# tasks = [asyncio.create_task(scrape_kobyla()), asyncio.create_task(scrape_pivovarske_domy()),
	# 		asyncio.create_task(scrape_ulva()), asyncio.create_task(scrape_sportcafe())]
	# await asyncio.gather(*tasks)


	await asyncio.gather(scrape_sportcafe())

if __name__ == "__main__":
	asyncio.run(start_scraping())

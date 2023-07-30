import asyncio
from Restaurants.PivovarskeDomy import PivovarskeDomy
from Restaurants.Kobyla import Kobyla
from Restaurants.Ulva import Ulva
from Restaurants.SportCafe import SportCafe


async def scrape_pivovarske_domy():
    pivovarske_domy = PivovarskeDomy()
    await pivovarske_domy.scrape_data()
    print(pivovarske_domy.name)
    for key, values in pivovarske_domy.menu.items():
        print(key)
        for value in values:
            print(value)
        print("\n")


async def scrape_kobyla():
    kobyla = Kobyla()
    await kobyla.scrape_data()
    print(kobyla.name)
    for day, menu in kobyla.menu.items():
        print(day)
        print(menu)


async def scrape_ulva():
    ulva = Ulva()
    await ulva.scrape_data()
    print(ulva.name)
    for x, y in ulva.menu.items():
        print(x, y)


async def scrape_sportcafe():
    sport_cafe = SportCafe()
    await sport_cafe.scrape_data()
    print(sport_cafe.name)
    for key, values in sport_cafe.menu.items():
        print(key)
        for value in values:
            print(value)
        print("\n")


async def start_scraping():
    tasks = [asyncio.create_task(scrape_kobyla()), asyncio.create_task(scrape_pivovarske_domy()),
             asyncio.create_task(scrape_ulva()), asyncio.create_task(scrape_sportcafe())]
    results = await asyncio.gather(*tasks)

    # await asyncio.gather(asyncio.create_task(scrape_ulva()))

if __name__ == "__main__":
    asyncio.run(start_scraping())

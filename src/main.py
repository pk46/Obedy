import asyncio
from restaurants.pivovarske_domy import PivovarskeDomy
from restaurants.kobyla import Kobyla
from restaurants.u_lva import Ulva
from restaurants.sport_cafe import SportCafe
from utilities.html_generator import HTMLGenerator


async def scrape_pivovarske_domy():
    pivovarske_domy = PivovarskeDomy("https://restaurace.pivovarskedomy.cz/denni-menu", "Pivovarské domy")
    await pivovarske_domy.main()
    return pivovarske_domy.menu, pivovarske_domy.name


async def scrape_kobyla():
    kobyla = Kobyla("https://kobylahradec.cz/poledni-menu/", "Kobyla")
    await kobyla.main()
    return kobyla.menu, kobyla.name


async def scrape_ulva():
    ulva = Ulva("http://www.ulvahk.cz/denni-menu/", "U Lva")
    await ulva.main()
    return ulva.menu, ulva.name


async def scrape_sportcafe():
    sport_cafe = SportCafe("https://www.sport-cafe.cz/#tydenni-menu", "Sport Café")
    await sport_cafe.main()
    return sport_cafe.menu, sport_cafe.name


async def start_scraping():
    # tasks = [asyncio.create_task(scrape_kobyla()), asyncio.create_task(scrape_pivovarske_domy()),
    #          asyncio.create_task(scrape_ulva()), asyncio.create_task(scrape_sportcafe())]
    # results = await asyncio.gather(*tasks)

    result = await asyncio.gather(asyncio.create_task(scrape_sportcafe()))
    generator = HTMLGenerator(result[0][1])
    result = generator.generate_html(result[0])

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(result)
    

if __name__ == "__main__":
    asyncio.run(start_scraping())

import asyncio
from restaurants.pivovarske_domy import PivovarskeDomy
from restaurants.kobyla import Kobyla
from restaurants.restaurant import Restaurant
from restaurants.u_lva import Ulva
from restaurants.sport_cafe import SportCafe
from utilities.html_generator import HTMLGenerator

restaurants = [
    PivovarskeDomy("https://restaurace.pivovarskedomy.cz/denni-menu", "Pivovarské domy"),
    Kobyla("https://kobylahradec.cz/poledni-menu/", "Kobyla"),
    Ulva("http://www.ulvahk.cz/denni-menu/", "U Lva"),
    SportCafe("https://www.sport-cafe.cz/#tydenni-menu", "Sport Café")
]


async def scrape(restaurant: Restaurant):
    await restaurant.main()
    return restaurant.menu, restaurant.name


async def start_scraping():
    tasks = [asyncio.create_task(scrape(restaurant)) for restaurant in restaurants]
    results = await asyncio.gather(*tasks)
    
    generator = HTMLGenerator()
    html = generator.generate_html(results)
    
    with open("index.html", "w", encoding="utf-8") as file:
        
        file.write(html)


if __name__ == "__main__":
    asyncio.run(start_scraping())

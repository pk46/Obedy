import asyncio

from restaurants.archway import Archway
from restaurants.cerny_kun import CernyKun
from restaurants.duran import Duran
from restaurants.mexita import Mexita
from restaurants.pivovarske_domy import PivovarskeDomy
from restaurants.kobyla import Kobyla
from restaurants.potrefena_husa import PotrefenaHusa
from restaurants.restaurant import Restaurant
from restaurants.u_lva import Ulva
from restaurants.sport_cafe import SportCafe
from utilities.html_generator import HTMLGenerator

restaurants = [
    PivovarskeDomy("https://restaurace.pivovarskedomy.cz/denni-menu", "Pivovarské domy"),
    Kobyla("https://kobylahradec.cz/poledni-menu/", "Kobyla"),
    Ulva("http://www.ulvahk.cz/denni-menu/", "U Lva"),
    SportCafe("https://www.sport-cafe.cz/#tydenni-menu", "Sport Café"),
    Archway("https://www.archwayrestaurant.cz/tydenni-menu/", "Archway"),
    Duran("https://www.duran.cz/tydenni-menu/", "Restaurant Duran"),
    PotrefenaHusa("https://husahradec.cz/tydenni-menu", "Potrefená husa"),
    Mexita("https://www.mexita.cz/tydenni-menu", "Mexita"),
    CernyKun("http://www.cernykunhk.cz/tydenni-menu", "Černý kůň"),
]


async def scrape(restaurant: Restaurant):
    await restaurant.main()
    return restaurant.menu, restaurant.name, restaurant.url


async def start_scraping():
    tasks = [asyncio.create_task(scrape(restaurant)) for restaurant in restaurants]
    results = await asyncio.gather(*tasks)
    
    generator = HTMLGenerator()
    html = generator.generate_html(results)
    
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html)


if __name__ == "__main__":
    asyncio.run(start_scraping())

import time

from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from restaurants.restaurant import Restaurant
from selenium import webdriver


class PotrefenaHusa(Restaurant):
    def __init__(self, url, name):
        super().__init__(url, name)
    
    def _process_data(self, data):
        date = data[0].find("div", {"class": "row justify-content-center flex-wrap"}).find("p")
        week_food = data[0].find("div", {"class": "men-integ-web__foods-wrapper"})
        # print(data)
        ...
    
    async def main(self):
        options = webdriver.EdgeOptions()
        options.add_argument('--headless')
        browser = webdriver.Edge(options=options)
        
        try:
            browser.get(self._url)
            browser.switch_to.frame(0)
            elements = WebDriverWait(browser, 10).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, "men-integ-web__day"))
            )
            for element in elements[:-2]:
                print(element.text)
        except TimeoutException:
            print("I give up...")  # nahradit loggerem
        finally:
            browser.quit()
        scraped_data = await self._scrape_data()
        # if scraped_data:
        #     self._process_data(scraped_data)
        # else:
        #     self._menu["Chyba"] = ["Chyba při načítání dat"]

from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
    async def main(self, ec=None):
        options = webdriver.EdgeOptions()
        # options.add_argument('--headless')
        
        browser = webdriver.Edge(options=options)
        
        try:
            browser.get(self._url)
            script = """
            (function(e,n,t,a,s){a=e.getElementsByTagName("head")[0],(s=e.createElement("script")).async=1,s.src="https://menickator.cz/integrations/web/includes/OqYRmcNHTZkNVT0yKXLj.js",a.appendChild(s)}(document));
            """
            
            browser.execute_script(script)
            
            # Počkejte, dokud skript neskončí
            timeout_in_seconds = 10
            WebDriverWait(browser, timeout_in_seconds).until(
                EC.presence_of_element_located((By.CLASS_NAME, "men-integ-web text-align-center"))
            )
            
            html = browser.page_source
            print(html)
            # soup = BeautifulSoup(html, features="html.parser")
            # print(soup)
        except TimeoutException:
            print("I give up...")
        finally:
            browser.quit()
        scraped_data = await self._scrape_data()
        # if scraped_data:
        #     self._process_data(scraped_data)
        # else:
        #     self._menu["Chyba"] = ["Chyba při načítání dat"]

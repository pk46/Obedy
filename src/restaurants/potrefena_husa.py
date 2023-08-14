import logging

from bs4 import BeautifulSoup
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from restaurants.restaurant import Restaurant
from selenium import webdriver

from utilities.request_helper import RetryableHttpError


class PotrefenaHusa(Restaurant):
    __MAX_RETRIES = 5
    
    def __init__(self, url, name):
        super().__init__(url, name)
        self.__date = ""
        logging.basicConfig(filename="../scraper.log",
                            format=self.FORMAT,
                            level=logging.INFO,
                            encoding="utf-8",
                            filemode="a")
        self.logger = logging.getLogger()
        self.__options = webdriver.EdgeOptions()
        self.__options.add_argument('--headless')
    
    async def __get_url(self, url):
        for retry in range(1, self.__MAX_RETRIES + 1):
            try:
                self.__browser = webdriver.Edge(options=self.__options)
                self.logger.info(f"{self._name}: Selenium headless browser started")
                self.__browser.get(url)
                self.__date = self.__browser.execute_script("return document.getElementsByTagName('p');")[1].text
                self.__browser.switch_to.frame(0)  # iFrame with food is on index 0
                
                WebDriverWait(self.__browser, 10).until(
                    ec.presence_of_all_elements_located((By.CLASS_NAME, "men-integ-web__day"))
                )
                return self._process_data(self.__browser.page_source)
            except TimeoutException:
                logging.error(f"{self._name}: požadovaný element nebyl na stránce nalezen ")
                if retry == self.__MAX_RETRIES:
                    raise RetryableHttpError("Všechny pokusy selhaly vyjímkou. Poslední: ", "WebDriverException")
            except WebDriverException as e:
                logging.error(f"{self._name}: pokus č. {retry} selhal chybou WebDriverException {e.msg}")
                if retry == self.__MAX_RETRIES:
                    raise RetryableHttpError(f"Všechny pokusy selhaly vyjímkou. Poslední:  {e.msg}", self.__class__)
            except Exception as error:
                logging.error(f"{self._name} pokus č. {retry} selhal chybou: {error}")
                return None
            finally:
                self.__browser.quit()
                self.logger.info(f"{self.name}: Selenium headless browser exited.")
    
    def _process_data(self, data):
        menu = BeautifulSoup(data, "lxml")
        days = menu.findAll("div", {"class": "men-integ-web__day"})[:-2]  # -2 = except Weekend
        for i in range(len(days)):
            daily_menu = days[i]
            day_value = daily_menu.find("h3", {"class": "men-integ-web__subtitle"}).text
            food_elements = daily_menu.findAll("p", {"class": "men-integ-web__food"})
            food_value = [food.text for food in food_elements]
            self._menu[f"{day_value}  {self.__date}"] = food_value
            
    async def main(self):
        try:
            scraped_data = await self.__get_url(self._url)
            if scraped_data:
                self._process_data(scraped_data)
        except Exception as e:
            logging.error(f"Chyba při načítání dat: {e}")
            self._menu["Chyba"] = ["Chyba při načítání dat"]

from abc import ABC, abstractmethod
from lib.request_parser import parse_filename
from lib.drivers import SeleniumWireDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from io import BytesIO
import gzip
import json

class Scraper(ABC):
    def __init__(self, search_url, driver):
        self.search_url = search_url
        self.driver = driver

    @abstractmethod
    def search(self, query):
        pass

    @abstractmethod
    def get_products(self):
        pass

class ScraperEnjoei(Scraper):
    def __init__(self):
        super().__init__("https://enjoei.com.br", SeleniumWireDriver().get_driver())

    def search(self, query):
        driver = self.driver
        driver.get(self.search_url)

        search_box = driver.find_element(By.CLASS_NAME, "search-input__input")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

    def get_products(self, query):
        self.search(query)

        while True:
            for request in self.driver.requests:
                if parse_filename(request) == "graphql-search-x" and request.method == "GET" and request.response.status_code == 200:
                    compressed_body = BytesIO(request.response.body)
                    
                    with gzip.GzipFile(fileobj=compressed_body) as f:
                        decompressed_body = f.read()
                    payload = json.loads(decompressed_body.decode('utf-8')) # acentos

                    self.driver.quit()
                    return json.dumps(payload, indent=4, ensure_ascii=False)
                
    #TODO: paginação
                            
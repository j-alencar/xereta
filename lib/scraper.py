from abc import ABC, abstractmethod
from lib.request_parser import parse_filename
from lib.drivers import SeleniumWireDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from io import BytesIO
import requests
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
        self.driver.get(self.search_url)

        search_box = self.driver.find_element(By.CLASS_NAME, "search-input__input")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

    def get_total(self, request):
        compressed_body = BytesIO(request.response.body)
                    
        with gzip.GzipFile(fileobj=compressed_body) as f:
            decompressed_body = f.read()

        temp_json = json.loads(decompressed_body)

        total = temp_json['data']['search']['products']['total'] # número real de resultados
        return total

    def get_true_json(self, request):
        total = self.get_total(request)
        true_url = request.url.replace("first=30", f"first={total}")
        r = requests.get(true_url)
        return r.json()

    def get_products(self, query):
        self.search(query)

        while True:
            for request in self.driver.requests:
                if parse_filename(request) == "graphql-search-x" and request.method == "GET" and request.response.status_code == 200:
                    self.driver.quit()

                    return self.get_true_json(request)
                else:
                    continue                            
from abc import ABC, abstractmethod
from seleniumwire import webdriver

class WebDriver(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_driver(self):
        pass

class SeleniumWireDriver(WebDriver):
    def __init__(self):
        self.seleniumwire_options = {
            'enable_har': True,
        }
        self.chrome_options = webdriver.ChromeOptions()
        self.set_headless()
        self.driver = webdriver.Chrome(seleniumwire_options=self.seleniumwire_options, options=self.chrome_options)

    def set_headless(self):
        self.chrome_options.add_argument("--headless")
        
    def get_driver(self):
        return self.driver
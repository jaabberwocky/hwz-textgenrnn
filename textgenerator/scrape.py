import requests
from bs4 import BeautifulSoup as bs
import hwzscrape as hz

class Scrapper:
    type = None
        
    def __init__(self, target):
        self.__target = target

    def getTarget(self):
        return self.__target

    def setTarget(self, target):
        self.__target = target
        return None
    
class HWZScrapper(Scrapper):
    type = 'HWZ'

    def 
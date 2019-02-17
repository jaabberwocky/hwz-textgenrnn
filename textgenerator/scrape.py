"""
Contains Scrapper classes
"""
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import re
import os

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
    def __init__(self):
        self.type = 'HWZ'
        self.scrappedContent = []
    
    def getURL(self, args):
        '''
            gets URL from arguments parsed to CLI

            Args: args [arguments from parser]
        '''
        url = args.URL
        return url

    def getPageHTML(self, url):
        '''
            Opens connection and gets HTML

            Args: url
        '''
        client = urlopen(url)
        page_html = client.read()
        client.close()
        return page_html


    def getPageSoup(self, page_html):
        '''
        Parses HTML to get Soup

        Args: page_html
        '''
        return soup(page_html, "html.parser")


    def getPageNumbers(self, page_soup):
        '''
            Gets page numbers from soup object.

            Args: page_soup
        '''
        y = page_soup.find("div", {"class": "pagination"})
        if y is None:
            # this means that it is single page !
            total_pages = 1
        else:
            total_pages = int(y.span.text.split(" ")[-1])
        return total_pages


    def getPosts(self, page_soup):
        '''
            Gets all posts from soup object.

            Args: page_soup
        '''
        return page_soup.findAll("div", {"class": "post-wrapper"})

    def scrapeThread(self, url):
        '''
        Scrapes an entire thread and returns all the posts
        '''

        my_url = url

        # get initial page soup and html
        page_html = self.getPageHTML(my_url)
        page_soup = self.getPageSoup(page_html)
        total_pages = self.getPageNumbers(page_soup)

        # loop for page
        pg = 1
        count = 0

        # initialise lists
        content_list = []
       
        while pg <= total_pages:
            print("Scrapping page: ", pg, "....")
            url_loop = my_url.split(".html")[0] + '-' + str(pg) + ".html"
            pg += 1

            page_html = self.getPageHTML(url_loop)
            page_soup = self.getPageSoup(page_html)

            posts = self.getPosts(page_soup)

            for post in posts:
                count += 1
                post_content = post.find("div", {"class": "post_message"}).text
                content_list.append(post_content)
        
        return content_list

    def scrapeForum(self, url):
        root = "https://forums.hardwarezone.com.sg"
        threadQueue = Queue.Queue()
        
        # get initial page soup and html
        page_html = self.getPageHTML(url)
        page_soup = self.getPageSoup(page_html)

        # get pagination
        numPages = int(page_soup.find("div", {"class":"pagination"}).find("span").text.split(" ")[-1])
        pageCounter = 1
        
        while pageCounter <= numPages:
            threadListingURL = url + "index%d.html" % pageCounter
            print("Scrapping forum listing %s..." %threadListingURL)
            page_html = self.getPageHTML(threadListingURL)
            page_soup = self.getPageSoup(page_html)

            # get threads
            threads = page_soup.find_all("a", {"id":re.compile("thread_title*")})
            for t in threads:
                threadQueue.put(t)

            while !threadQueue.empty():
                q = threadQueue.get()
                print("Scrapping thread %s" % t)
                self.scrappedContent.append(self.scrapeThread(root + t['href']))

            pageCounter += 1

        return None

    def writeScrappedContent(self):
        '''
        Writes scrapped content to text file.
        '''
        if os.path.isfile("scrappedText.txt"):
            os.remove("scrappedText.txt")
        f = open("scrappedText.txt", "w")

        for s in self.scrappedContent:
            f.write(s+"\n")
        f.close()
        return None

        
       
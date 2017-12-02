import os
import json
import requests
from lxml import html
from functools import lru_cache
import uuid
import time


# Multi processing
# https://docs.python.org/3.6/library/threading.html#using-locks-conditions-and-semaphores-in-the-with-statement


# PROXY NOTES
# 1. http://www.doc.ic.ac.uk/~pg1712/blog/python-proxy/

class Site:
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4)
        self.urls = set()
        self.crawl_count = 0

    ###################################### Format URL
    def format_url(self, url):
        # Check/Format URL
        # check for no subdomain
        if(url[-1] == "/"):
            url = url[:-1]

        if(url.count(".") < 2):
            # print("invalid url")
            return "invalid url"
        if(url.find("://") > 0 ):
            # print("protocol included")
            full_url = url
        else:
            # print("no protocol")
            full_url = "https://" + url
        return full_url
    ###################################### Run Crawler
    # @lru_cache(maxsize=1000)
    def run_crawler(self, url):
        self.crawl_count += 1
        # ensure proper url formating
        url = self.format_url(url)
        # GEN LINK INSTANCE
        page = Page(url)

        self.urls.add(page.url)

        page.add_page_content()
        page.add_links()

        links_len = len(page.links)
        # print("Crawled: {}".format(self.urls))
        for link in page.links:
            # print("checking link {}".format(links[i]))
            if link not in self.urls:
                # print(link)
                self.run_crawler(link)
                # print("found")
                # print("link not found: {}".format(page.links[i]))
                # run_crawler(page.links[i])


class Page:
    def __init__(self, url):
        if(url[-1] == "/"):
            url = url[:-1]
        self.url = url
        self.id = str(uuid.uuid4())
        self.links = set()
        self.page = ""
        self.valid = True
    def __str__(self):
        return self.url

    ###################################### Add Page Content
    def add_page_content(self, **kwargs):
        if "proxies" not in kwargs:
            proxies=None
        else:
            proxies= kwargs['proxies']

        if "headers" not in kwargs:
            headers=None
        else:
            headers = kwargs['headers']

        # print("self.url: {}".format(self.url))
        r = requests.get(self.url, proxies=proxies, headers=headers)

        # print(r.headers)
        payload = dict()
        payload['content'] = r.content

        # SET PAGE CONTENT
        self.page = html.fromstring(r.content)

    ###################################### Parse Links on Page
    def add_links(self):
        #create a list of links:
        all_links = self.page.xpath('//a/@href')
        abs_links = []
        links = []

        # separate absolute and relatie links
        for link in all_links:
            # check for relative link
            if(link[0] == "/"):
                # print("ADDED rel: {}".format(link))
                # ADD relative links to payload
                link = self.url + link
                links.append(link)
            # filter out section links, and comm links
            elif(link[0] == "#"):
                # print("SKIPPED #: {}".format(link))
                pass
            elif(link.find("tel:") < 0 and link.find("mailto:") < 0):
                # add absolute links to abs_links
                abs_links.append(link)
                # print("ADDED abs: {}".format(link))
            else:
                pass
                # print("SKIPPED: {}".format(link))

        # check host of abs_links
        for link in abs_links:
            if(link.find(url) > -1):
                # print("SAMEHOST: {}".format(link))
                link = link
                links.append(link)

        # printlinks for debugging
        # print(self.url)
        # print("links: ")
        for link in links:
            if(link[-1] == "/"):
                # trim / off of end
                link = link[:-1]
            # print("     {}".format(link))
            self.links.add(link)


# url = input("enter a url: ->  ")
url = "www.yourpianoservice.com/"


site = Site(url)
start = time.time()
site.run_crawler(url)
end = time.time()

run_time = end - start


print("site: {}\n{}\n\n{}".format(site.name, site.id, site.urls))

print("performance metrics:\n\ntime: {}\ncrawl count: {}\nlinks count: {}".format(run_time, site.crawl_count, len(site.urls)))

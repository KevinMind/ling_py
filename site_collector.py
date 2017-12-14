import os
from lxml import html
import requests
import uuid
import json
import datetime


import save_to_file as scribe
import site_crawl as crawler

class SiteCollector:
    def __init__(self, name):
        self.name = name
        self.proxies = self.gen_proxies()
        self.id = str(uuid.uuid4())
        self.data_file = scribe.init_file(self.name, self.id)
        self.error_file = ""
        self.query = "how to make binary trees in python"
        self.query_count = 0
    def __str__(self):
        return self.name
    def time_stamp(self):
        return scribe.time_stamp()
    def gen_proxies(self):
        http_proxy  = "http://10.10.1.10:3128"
        https_proxy = "https://10.10.1.11:1080"
        ftp_proxy   = "ftp://10.10.1.10:3128"

        proxyDict = {
          "http"  : http_proxy,
          "https" : https_proxy,
          "ftp"   : ftp_proxy
        }
        return proxyDict
    def search_google(self, queries):
        for query in queries:
            # REQUEST
            # PROXY NOTES
            # 1. http://www.doc.ic.ac.uk/~pg1712/blog/python-proxy/

            s = requests.session()
            # s.proxies.update(proxies)

            # search = input("search: =>\n")
            url = 'https://www.google.com/search?q={}'.format(query)
            r = requests.get(url)

            # RESPONSE
            r_status = r.status_code
            #### HEADERS
            r_headers = r.headers
            r_date = r_headers["Date"]

            print("PINGING... GOOGLE: {} STATUS: {}".format(self.query_count, r_status))

            #### HANDLE ERROR
            if(r_status != 200):
                error_obj = r.content
                # error_obj['id'] = TIME_STAMP
                self.error_file = scribe.write_error(name, self.id, error_obj)
                print(r.headers)
                return

            #### HANDLE SUCCESS
            if(r_status == 200):
                r_tree = html.fromstring(r.content)

                #create a list of links:
                results = r_tree.xpath("//h3[contains(@class, 'r')]/a/@href")

                # r_tree playground
                # results_2 = r_tree.xpath("//div[contains(@class, 'r')]")
                # links = r_tree.xpath('///a/@href')

                # Generate list of links
                links_list = []
                for link in results:
                    # define separator
                    sep = "&sa="
                    # clean link: trim firts seven characters and split by sep, keeping first portion
                    clean = link[7:].split(sep, 1)[0]
                    links_list.append(clean)
                    print(clean)

                payload = dict()

                payload["id"] = str(uuid.uuid4())
                payload["status_code"] = r_status
                payload["date"] = r_date
                payload["search"] = query
                payload["count"] = len(links_list)
                payload["links"] = links_list

                print("response: COUNT: {}".format(len(links_list)))
                scribe.read_write(self.data_file, payload)

    def crawl_sites(self, sites):
        for site in sites:
            site = crawler.make_site(site)
            site.run_crawler(site.name)
    def parse_data_file(self):
        working_file = scribe.read_file(self.data_file)
        queries = working_file["data"]
        for query in queries:
            self.crawl_sites(query['links'])



name = input("job name... keep it short, no spaces.")
site = SiteCollector(name)

site.search_google(["set data type in javascript"])

site.parse_data_file()

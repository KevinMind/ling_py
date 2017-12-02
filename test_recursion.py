import random
import uuid

# create lists of numbers
sites = []

names = [
    "/about",
    "/blog",
    "/post",
    "/billy",
    "/julie",
    "/hello",
    "/new-jouiisey"
]

class Site:
    def __init__(self, name):
        self.name = name
        self.links = []

    def __str__(self):
            return str(self.name)

    def make_links(self, sites):
        count = random.randrange(1, len(sites))
        for x in range(0, count):
            self.links.append(sites[x])
        print("{}: {}".format(self.name, len(self.links)))
        for link in self.links:
            print("     {}".format(link.name))

# Generate sites
len_names = len(names)

for x in range(0, len_names):
    site = Site(names[x])
    sites.append(site)
    # print(site.id)

sites_len = len(sites)
# print("sites generated:\n\n")
# Generate links between sites
for x in range(0, sites_len):
    # print("generating links fro site {}".format(sites[x].id))
    sites[x].make_links(sites)

# create search function
for x in sites:
    print(x.name)

crawled_sites = set()
def crawl_site(link):
    print("crawling page: {}".format(link))
    crawled_sites.add(link)
    print("already have crawled: {}".format(crawled_sites))
    print("this site has {} links. begin crawl.".format(len(site.links)))
    for x in range(0, len(link.links)):
        if link.links[x] not in crawled_sites:
            print("{}. new link found: {}".format((x + 1), link.links[x].name))
            crawl_site(link.links[x])


def run_crawler(sites):
    print("start crawler\n")
    start = random.randrange(0, len(sites))
    print("starting with {}".format(sites[start]))
    crawl_site(sites[start])

run_crawler(sites)

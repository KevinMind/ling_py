import os
from lxml import html
import requests
import uuid
import json
import datetime

# CREATE DUMP FILE
TIME_STAMP = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
JOB_ID = str(uuid.uuid4())

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) #<-- absolute dir the script is in
print("Current directory : {}".format(CURRENT_DIR))
REL_NAME = "data/data-{}.json".format(TIME_STAMP)
DATA_FILENAME = os.path.join(CURRENT_DIR, REL_NAME)
print(DATA_FILENAME)

# INITIALIZE FILE
with open(DATA_FILENAME, 'w+') as f:
    json.dump([{"job_id": JOB_ID}], f)

# CREATE FOREVER LOOP


# Initialize Counter
counter = 0
while True:
    counter += 1

    # REQUEST

    # PROXY NOTES
    # 1. http://www.doc.ic.ac.uk/~pg1712/blog/python-proxy/

    s = requests.session()
    # s.proxies.update(proxies)

    http_proxy  = "http://10.10.1.10:3128"
    https_proxy = "https://10.10.1.11:1080"
    ftp_proxy   = "ftp://10.10.1.10:3128"

    proxyDict = {
      "http"  : http_proxy,
      "https" : https_proxy,
      "ftp"   : ftp_proxy
    }


    # search = input("search: =>\n")
    search = "how to peel a banana"
    url = 'https://www.google.com/search?q={}'.format(search)
    r = requests.get(url)



    # RESPONSE
    r_status = r.status_code
    #### HEADERS
    r_headers = r.headers
    r_date = r_headers["Date"]

    print("PINGING... GOOGLE: {} STATUS: {}".format(counter, r_status))

    #### HANDLE ERROR
    if(r_status != 200):
        error_obj = r.content
        # error_obj['id'] = TIME_STAMP
        ERROR_FILENAME = "error/error-{}.txt".format(JOB_ID)
        with open(ERROR_FILENAME, 'wb') as f:
            f.write(error_obj)
        print(r.headers)
        break

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

        # INSPECT BODY
        # list_length = len(links_list)
        # for x in range(1, (list_length)):
        #     print("{}. {}".format(x, links_list[x]))


        payload = dict()

        payload['id'] = str(uuid.uuid4())
        payload['status_code'] = r_status
        payload['date'] = r_date
        payload['search'] = search
        payload['body'] = {
            "count": len(links_list),
            "contents": links_list
        }

        print("response: COUNT: {}".format(len(links_list)))

        # READ DATA
        with open(DATA_FILENAME) as f:
            data = json.load(f)

        # UPDATE DATA
        data.append(payload)

        # WRITE DATA
        with open(DATA_FILENAME, 'w') as f:
            json.dump(data, f)

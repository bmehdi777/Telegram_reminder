import urllib.request
import json
import xmltodict
import datetime


def get_guide():
    time = datetime.datetime.now()
    url_channel = "https://xmltv.ch/xmltv/xmltv-tnt.xml"

    x  = urllib.request.urlopen(url_channel).read()
    o = xmltodict.parse(x)

    return o

    """for i in o["rss"]["channel"]["item"]:
        if ("TF1" in i["title"]):
            print(i["title"].split("|"))"""

if __name__ == "__main__":
    print(get_guide())
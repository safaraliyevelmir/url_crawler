from simplified_scrapy.spider import Spider, SimplifiedDoc


class DemoSpider(Spider):
    name = "demo-spider"
    start_urls = ["https://jobs.glorri.az/"]
    allowed_domains = ["jobs.glorri.az"]

    def extract(self, url, html, models, modelNames):
        doc = SimplifiedDoc(html)
        lstA = doc.listA(url=url["url"])
        print(lstA)
        exit()
        return [{"Urls": lstA, "Data": None}]

settings = {
    "concurrency": 10, 
    "concurrencyPer1S": 20,
    "intervalTime": 0.1,  
    "max_workers": 20,
    "refresh_tm": 30,
    "disable_extract": False, 
    "request_tm": 10,  
}


from simplified_scrapy.simplified_main import SimplifiedMain

SimplifiedMain.startThread(DemoSpider(), setting=settings)

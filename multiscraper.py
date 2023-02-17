import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http.request import Request
from urllib.parse import urlparse
import json 

output = {}

class AmplifypartnersSpider(scrapy.Spider):
  name = "amplifypartners"
  start_urls = ['https://www.amplifypartners.com/portfolio']

  def parse(self, response):
    baseUrl = ".".join(urlparse(response.url).netloc.split(".")[-2:])
    output[baseUrl] = []
    for listItem in response.css("div.w-dyn-item"):
      itemStatus = listItem.css("div.status-div").css("div::text").get()
      itemDomain = listItem.css("div.website__link-wr").css("a::text").get()
      try:
        if itemStatus == None:
            raise Exception("Company Status is empty")
        if itemDomain == None:
            raise Exception("Company Domain is empty")        
        if "active" in itemStatus.lower():
          output[baseUrl].append(itemDomain)
      except Exception as error:
        print("Could not process %s from %s: %s" % (itemDomain, response.url, error))        

class LsvpSpider(scrapy.Spider):
  name = "lsvp"
  start_urls = ['https://lsvp.com/portfolio']

  custom_settings = {
      'DOWNLOAD_DELAY': 0.1,
  }
  
  domainList = []

  def parse(self, response):
    baseUrl = ".".join(urlparse(response.url).netloc.split(".")[-2:])
    output[baseUrl] = []
    for listItem in response.css("div.portfolio-item"):
      itemStatus = listItem.css("strong.subtitle::text").get()
      itemDomain = listItem.css("span.url::text").get()
      try: 
        if itemStatus == None:
          raise Exception("Company Status is empty")
        if itemDomain == None:
          raise Exception("Company Domain is empty")          
        if "public" not in itemStatus.lower() and "acquired" not in itemStatus.lower():
          output[baseUrl].append(itemDomain)
      except Exception as error:
        print("Could not process %s from %s: %s" % (itemDomain, response.url, error))
    
    # I could have used a LinkExtractor here but decided it was better to be specific
    for linkItem in response.css("li.column"):
      linkUrl = linkItem.css("a").xpath("@href").get()
      yield Request(linkUrl, callback=self.parsePortfolio)
  
  def parsePortfolio(self, response):
    baseUrl = ".".join(urlparse(response.url).netloc.split(".")[-2:])
    for listItem in response.css("div.portfolio-content"):
      itemStatus = listItem.css("h4::text").get()
      itemDomain = listItem.css("a::text").get()
      try: 
        if itemStatus == None:
          raise Exception("Company Status is empty")
        if itemDomain == None:
          raise Exception("Company Domain is empty")
        if "public" not in itemStatus.lower() and "acquired" not in itemStatus.lower():
          output[baseUrl].append(itemDomain)
      except Exception as error:
        print("Could not process %s from %s: %s" % (itemDomain, response.url, error))

process = CrawlerProcess()
process.crawl(AmplifypartnersSpider)
process.crawl(LsvpSpider)
process.start()

## sort and deduplicate lists
for key in output:
  tempList = list(dict.fromkeys(output[key]))
  tempList.sort()
  output[key] = tempList

print("=================")
print("Requested Output:")
print(json.dumps(output, indent=2))
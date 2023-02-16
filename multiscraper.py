import scrapy
from scrapy.crawler import CrawlerProcess
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
      itemUrl = listItem.css("div.website__link-wr").css("a::text").get()
      if itemStatus != None and "active" in itemStatus.lower():
        output[baseUrl].append(itemUrl)

class LsvpSpider(scrapy.Spider):
  name = "lsvp"
  start_urls = ['https://lsvp.com/portfolio']

  def parse(self, response):
    baseUrl = ".".join(urlparse(response.url).netloc.split(".")[-2:])
    output[baseUrl] = []
    for listItem in response.css("div.portfolio-item"):
      itemStatus = listItem.css("strong.subtitle::text").get()
      itemUrl = listItem.css("span.url::text").get()
      if itemStatus != None and "public" not in itemStatus.lower() and "acquired" not in itemStatus.lower():
        output[baseUrl].append(itemUrl)

process = CrawlerProcess()
process.crawl(AmplifypartnersSpider)
process.crawl(LsvpSpider)
process.start()

print("=================")
print("Requested Output:")
print(json.dumps(output, indent=2))
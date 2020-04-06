import scrapy

class PypPISpider(scrapy.Spider):
    name = "PyPI_spider"
    # url contains links to all pypi packages
    start_urls = ["https://pypi.org/simple/"]

    custom_settings = {
        'FEED_FORMAT': 'csv', # Format to save in
        'FEED_URI': 'data/pypi.csv' # Location to save in
    }
    
    def parse(self, response):
        # Gets all python packages on pypi
        PACKAGE_SELECTOR = "//a/text()"
        for package in response.xpath(PACKAGE_SELECTOR).extract():
            yield { "package": package }

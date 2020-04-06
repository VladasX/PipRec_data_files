import scrapy

class PythonProjectSpider(scrapy.Spider):
    name = "python_spider"
    start_urls = ["https://github.com/topics/python?l=python&s=updated"]

    custom_settings = {
        'FEED_FORMAT': 'csv', # Format to save in
        'FEED_URI': 'data/projects.csv', # Location to save in
        'AUTOTHROTTLE_ENABLED' : True,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }

    current_page = 0
    max_pages = 20 # Max number of pages to scrape

    def parse(self, response):
        self.current_page += 1

        # Selects all project boxes [author / project_name] (e.g. tensorflow / tensorflow)
        PROJECT_SELECTOR = "//h1[@class='f3 text-gray text-normal lh-condensed']"
        for project in response.xpath(PROJECT_SELECTOR):
            # Extracts url to project
            URL_SELECTOR = "a ::attr(href)"
            project_url = project.css(URL_SELECTOR).extract()[1] # [0] is author profile
            project_name = project_url[1:] # url contains author name and project name
            
            # Generate file urls
            yield {
                "project": project_name
            }

        # Go to the next page of projects (same as clicking 'Load more')
        if self.current_page < self.max_pages:
            # There is a hidden value used to list next projects
            LOAD_MORE_SELECTOR = "//input[@name='after']/@value"
            load_more = response.xpath(LOAD_MORE_SELECTOR).extract_first()
            if load_more:
                # Scrape the next page
                yield scrapy.Request(
                    "https://github.com/topics/python?l=python&s=updated&after=" + load_more,
                    callback=self.parse
                )

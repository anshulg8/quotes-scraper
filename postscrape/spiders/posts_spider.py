import scrapy
from unidecode import unidecode

class PostsSpider(scrapy.Spider):
    name = "posts"
    start_urls = [
        'https://www.goodreads.com/author/quotes/282885.Jordan_B_Peterson' #URL to scrape
    ]

    def parse(self, response):
        for post in response.css('div.quoteDetails'):
            quote = unidecode(post.css('.quoteText::text').get().strip())
            author = post.css('.authorOrTitle::text').get().strip().rstrip(',')
            if len(quote) + len(author) < 280:
                yield {
                    'quote': quote,
                    'author': author
                }
        next_page = response.css('a.next_pager::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

# To run, use command: scrapy crawl posts
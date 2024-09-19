import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            yield{
                'title' : book.css('h3 a').attrib['title'],
                'price' : book.css('.product_price .price_color::text').get(),
                'url' : book.css('h3 a').attrib['href']
            }

        next_page = response.css('li.next a::attr(href)').get() # to get the url to the next page

        if next_page is not None: # check if there're more next page
            if 'catalogue/' in next_page: # condition to check if the url is correct or not
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            
            # to go to the next page url with 'follow'
            # after that callback will execute after get the response from next page url
            # which is will execute the parse function again
            yield response.follow(next_page_url, callback=self.parse)
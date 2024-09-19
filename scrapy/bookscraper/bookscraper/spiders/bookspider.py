import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            relative_url = book.css('h3 a::attr(href)').get() # to get the url of the book

            if 'catalogue/' in relative_url: # condition to check if the url is correct or not
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            
            # to go to the book url with 'follow'
            # after that callback will execute after get the response from book url
            # which is will execute the parse_book_page function again
            yield response.follow(book_url, callback=self.parse_book_page)

    def parse_book_page(self, response):
        pass
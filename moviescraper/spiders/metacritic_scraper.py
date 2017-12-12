from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from items import Game

def safe_extract(selector, xpath_query):
    val = selector.xpath(xpath_query).extract()
    return val[0].strip() if val else 'NA'

class MetacriticSpider(Spider):
    """
    Goal : Scrape all movies from Horror genre
    1. Start URL : "http://www.metacritic.com/browse/movies/genre/date/action"
    Title
    Release Date
    Critic score
    User Score
    """

    name = "metacritic"
    allowed_domains = ["metacritic.com"]
    start_urls = [ "http://www.metacritic.com/browse/movies/genre/date/horror?view=condensed" ]

    # Get genre list from start_url, generate requests to parse genre pages later
    """
    def parse(self, response):
        genres = [s.split()[1].split('_',1)[1].replace("_","-") for s in response.xpath('//ul[@class="genre_nav"]/li/@class').extract()]
        genre_links = ["http://www.metacritic.com/browse/games/genre/date/"+ genre + "/pc" for genre in genres]

        requests = [Request(url = URL, callback = self.parse_genre) for URL in genre_links]
        self.log("###INITIAL PARSING###" + str(len(genre_links)) + "Genres IN THIS TOTAL LIST")
        return requests
    
    # Get all pages for a genre, send the to a page parser
    def parse_genre(self, response):
        try:
            page_links = [response.url + "?page=" + str(i) for i in range(int(response.xpath('//li[@class="page last_page"]/a/text()').extract()[0]))]
        except IndexError:
            page_links = [response.url]

        requests = [Request(url = URL, callback = self.parse_page) for URL in page_links]
        self.log("###PARSING GENRE###" + str(len(page_links)) + " PAGES IN THIS GENRE")
        return requests
    """
    # Get all games for a page
    def parse_page(self, response):
        game_links = ["http://metacritic.com" + postfix for postfix in
                      response.xpath('//ol[@class="list_products list_product_condensed"]/li/div/div/a/@href').extract()]
        meta_genre = response.xpath('//div[@class="module products_module list_product_condensed_module "]/div/div/h2[@class="module_title"]/text()').extract()[0].strip()
        requests = [Request(url = URL, callback = self.parse_game, meta = {'genre':meta_genre}) for URL in game_links ]
        self.log("###PARSING PAGE###" + str(len(game_links)) + " GAMES IN THIS PAGE")
        return requests

    def parse_game(self, response):
        sel = Selector(response, type = 'html')
        game = Game()

        # General Information
        game['title'] = safe_extract(sel, '//h3[@class="product_title"]/a/text()')
        game['link'] = response.url
        game['release_date'] = safe_extract(sel, '//li[@class="stat release_date"]/span[@class="data"]/text()')
        game['score'] = safe_extract(sel, '//li[@class="summary_detail developer"]/span[@class="data"]/text()')
        yield game
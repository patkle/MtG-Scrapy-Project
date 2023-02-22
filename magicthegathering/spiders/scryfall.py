from scrapy import Request, Spider


class scryfallSpider(Spider):
    name = "scryfall"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.pages = int(kwargs.get("pages", 10))

    def start_requests(self):
        for i in range(1, self.pages + 1):
            yield Request(f"https://scryfall.com/search?as=grid&order=name&page={i}&q=%2A%2A%2A&unique=cards")

    def parse(self, response):
        for card_id in response.xpath(".//div[@data-card-id]/@data-card-id").getall():
            yield Request(
                f"https://api.scryfall.com/cards/{card_id}",
                callback=self.parse_card
            )
    
    def parse_card(self, response):
        yield response.json()

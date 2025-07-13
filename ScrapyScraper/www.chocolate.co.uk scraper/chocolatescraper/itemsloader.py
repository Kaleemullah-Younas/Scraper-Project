from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


class chocolateproductloader(ItemLoader):

    default_output_processor = TakeFirst()
    price_in = MapCompose(lambda i: i.split("£")[-1])
    url_in = MapCompose(lambda x : 'https://www.chocolate.co.uk' + x)
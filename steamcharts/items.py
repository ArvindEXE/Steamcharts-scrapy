# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class SteamchartsItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class GameItem(scrapy.Item):
     Name = scrapy.Field()
     AppID = scrapy.Field()
     Month = scrapy.Field()
     Avg_players = scrapy.Field()
     Gain = scrapy.Field()
     Gain_percentage = scrapy.Field()
     Peak_players = scrapy.Field()

# WORK IN PROGRESS!

import scrapy
import pandas as pd

appids = pd.read_csv('/home/arvind/Documents/school/Thesis/appids.csv', usecols=['AppID'], index_col=False)
appid_list = appids['AppID'].to_list()


class SteamAppidScraperSpider(scrapy.Spider):
    name = "steam-appid-scraper"
    allowed_domains = ["steamcharts.com"]
    start_urls = ["https://steamcharts.com"]

    def parse(self, response):
        for appid in appid_list[:10]:   
            yield response.follow(
            url=response.urljoin('/app/' + str(appid)),
            callback=self.player_counts,
            meta={'appid' : appid}
        )

    def player_counts(self, response):
        game_name = response.css("h1#app-title  a::text").get()
        appid = response.meta['appid']
        for row in response.css('div.content table.common-table tbody tr'):
            data = row.css('td::text').getall()
            yield {
                'game': game_name,
                'appid': appid,
                'month': data[0].strip(),
                'avg. players': data[1],
                'gain': data[2],
                'gain precentage': data[3],
                'peak players': data[4],
            }


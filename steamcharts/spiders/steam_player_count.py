import scrapy
from steamcharts.items import GameItem

class SteamPlayerCountSpider(scrapy.Spider):
    name = "steam-player-count"
    allowed_domains = ["steamcharts.com"]
    start_urls = ["https://steamcharts.com/top/"]
    error_urls = []

    def parse(self, response):
        games = response.css("table#top-games tbody tr")
        for row in games:
            game = row.css("td.game-name.left a::text").get()
            appid = row.css("td.game-name.left a::attr('href')").get()
            yield response.follow(
                url=response.urljoin(appid),
                callback=self.player_counts,
                meta={'game': game, 'appid': appid}
            )

        page_url = 'https://steamcharts.com/top/p.{}'
        pages = 535 # 25 games per game, 535 are max pages as per 06/11/2023

        for i in range(1, pages+1):
            next_page_url = page_url.format(i)
            yield response.follow(next_page_url, callback=self.parse)

    def player_counts(self, response):
        game = response.meta['game']
        appid = response.meta['appid']
        game_item = GameItem()

        if response.status != 200:
            self.error_urls.append(response.url)

        for row in response.css('div.content table.common-table tbody tr'):
            data = row.css('td::text').getall()

            game_item['Name'] = game.strip()
            game_item['AppID'] = appid.split('/')[2]
            game_item['Month'] = data[0].strip()
            game_item['Avg_players'] = data[1]
            game_item['Gain'] = data[2]
            game_item['Gain_percentage'] = data[3]
            game_item['Peak_players'] = data[4]

            yield game_item

    def closed(self, reason):
        with open('error_urls.txt', 'w') as f:
            for url in self.error_urls:
                f.write(url + '\n')

    


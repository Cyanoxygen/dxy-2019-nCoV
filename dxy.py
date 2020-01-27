#!/usr/bin/env python3
from urllib import request
import datetime
import json

dxylink = 'https://3g.dxy.cn/newh5/view/pneumonia_peopleapp?from=timeline'
format_string = " {0:20} | {1:^10} | {2:^10} | {3:^10} | {4:^10} "
format_string_alt = "  | {0:17} | {1:^10} | {2:^10} | {3:^10} | {4:^10} "


class City:
    def __init__(self, source: dict):
        self.name = source['cityName']
        self.confirmed = source['confirmedCount']
        self.suspected = source['suspectedCount']
        self.dead = source['deadCount']
        self.cured = source['curedCount']

    def __str__(self):
        return f"""城市：{self.name}\n疑似病例：{self.suspected}\n确诊病例：{self.confirmed}\n死亡病例：{self.dead}\n治愈病例：{self.cured}"""

    def __repr__(self):
        return self.__str__()


class Area:
    def __init__(self, source: dict):
        self.name = source["provinceName"]
        self.confirmed = source['confirmedCount']
        self.suspected = source['suspectedCount']
        self.dead = source['deadCount']
        self.cured = source['curedCount']
        self.cities = []
        for n in source['cities']:
            self.cities.append(City(n))

    def __str__(self):
        return f"""地区：{self.name}\n疑似病例：{self.suspected}\n确诊病例：{self.confirmed}\n死亡病例：{self.dead}\n治愈病例：{self.cured}"""

    def __repr__(self):
        return self.__str__()


class News:
    def __init__(self, source: dict):
        self.id = source['id']
        self.date = datetime.datetime.fromtimestamp(source['pubDate'] / 1000)
        self.updateDate = source['pubDateStr']
        self.title = source['title']
        self.summary = source['summary']
        self.source = source['infoSource']
        self.url = source['sourceUrl']
        self.location = source['provinceName']

    def __str__(self):
        return f"{self.title}\n{self.updateDate} | {self.date}\n{self.location} | {self.source}\n{self.url}\n{self.summary}"

    def __repr__(self):
        return self.__str__()

    def markdown(self):
        return f"""**{self.title}**\n{self.updateDate} - {self.date}\n[{self.source}]({self.url}) | {self.location}\n{self.summary}"""


class Dxy:
    def __init__(self):
        self.Areas: list = []
        self.News: list = []
        try:
            respond = request.urlopen(dxylink).read().decode('utf-8')
        except request.HTTPError as e:
            print(f"获取数据出现错误：{e.__str__()}")
            return
        except request.http.client.IncompleteRead as e:
            print(f"获取数据出现意外的结尾：{e.__str__()}")
            return
        except Exception as e:
            print(f"获取数据时出现错误：{e.__str__()}")
            return

        details = respond.partition('<script id="getAreaStat">try { window.getAreaStat = ')[2] \
            .partition('}catch(e){}')[0]
        news = respond.partition('script id="getTimelineService">try { window.getTimelineService = ')[2] \
            .partition('}catch(e){}</script>')[0]
        details = json.loads(details)
        news = json.loads(news)

        for area_in_list in details:
            self.Areas.append(Area(area_in_list))

        for news_in_list in news:
            self.News.append(News(news_in_list))

    def printout(self):
        print(format_string.format('省份 / 城市', '疑似', '确诊', '死亡', '治愈'))
        for area in self.Areas:
            print(format_string.format(area.name, area.suspected, area.confirmed, area.dead, area.cured))

    def printall(self):
        print(format_string.format('省份 / 城市', '疑似', '确诊', '死亡', '治愈'))
        for area in self.Areas:
            print(format_string.format(area.name, area.suspected, area.confirmed, area.dead, area.cured))
            for city in area.cities:
                print(format_string_alt.format(city.name, city.suspected, city.confirmed, city.dead, city.cured))

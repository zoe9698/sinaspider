# -*- coding: utf-8 -*-
import scrapy
import time
from bs4 import BeautifulSoup
import csv
from ..items import SinaItem

class SinaspiderSpider(scrapy.Spider):
    name = 'sinaspider'
    allowed_domains = ['https://s.weibo.com']
    start_urls =[]
    # %E7%96%AB%E6%83%85=疫情
    # date = {
    #     '2019': {'12': ['15', '20', '23', '25', '28', '31']},
    #     '2020': {
    #         '1': [x for x in range(1, 32)],
    #         '2': [x for x in range(1, time.localtime(time.time())[2])]  # 每个月都要修改
    #     }
    # }
    date = {
        '2020': {'1': ['1', '25', '26', '27', '28', '29', '30', '31']},
        '2020': {
            '2': [x for x in range(1, time.localtime(time.time())[2])]  # 每个月都要修改
        }
    }
    for year in date.keys():
        for month in date[year].keys():
            for index in range(len(date[year][month]) - 1):
                start_time = str(year) + '-' + month + '-' + str(date[year][month][index])
                stop_time = str(year) + '-' + month + '-' + str(date[year][month][index + 1])
                for page in range(1,51):
                    # print('start_time:', start_time, '--stop_time:', stop_time)
                    url = 'https://s.weibo.com/weibo?q=%E6%96%B0%E5%9E%8B%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&typeall=1&suball=1&timescope=custom:' + start_time + ':' + stop_time + '&Refer=g&page=' + str(page)
                    start_urls.append(url)


    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        card_all = soup.find_all(attrs = {"action-type":"feed_list_item"})
        print(len(card_all))
        #f.write('\n---------------------------------第'+response.meta['page']+'页------------------------------\n')
        #f.write('\n------------------------------该页有'+str(len(card_all))+'条微博-----------------------------\n')
        for card in card_all:
            #try:
            #print('card:',card)
            time.sleep(1)
            soup = BeautifulSoup(str(card), 'lxml')
            nickname = soup.find('a', class_='name').text
            print('nickname:', nickname)
            txt = soup.find('p', class_='txt').text.strip()  # 转发的是列表，原创的好像不是列表
            #print('txt:', txt)
            date = (soup.select('.from > a'))[0].text.strip()
            print('date:', date)
            device = (soup.select('.from > a'))[1].text
            #print('device:', device)
            list = soup.select('ul > li > a')
            print(len(list))
            list = list[:5]
            for info in list:
                # print(info.text)
                item = info.text.replace(" ", '')
                if (item == ''):
                    like_count = 0
                elif (item[0] == '转'):
                    if (len(item) == 2):
                        forward_count = 0
                    else:
                        forward_count = item[2:]
                elif (item[0] == '评'):
                    if (len(item) == 2):
                        comment_count = 0
                    else:
                        comment_count = item[2:]
                elif (item[0] == '收'):
                    if (len(item) == 2):
                        favorate_count = 0
                    else:
                        favorate_count = item[2:]
                elif ((item[0] >= '0') and (item[0] <= '9')):
                    like_count = item[0:]
            item = SinaItem()
            item['nickname'] = nickname
            item['txt'] = txt
            item['date'] = date
            item['device'] = device
            item['favorate_count'] = favorate_count
            item['forward_count'] = forward_count
            item['comment_count'] = comment_count
            item['like_count'] = like_count
            # print(item)
            # time.sleep(5000)
            yield item
            # except Exception as e:
            #     print('**********************************************error**********************************************',e.args)
            #     #f.write(str(info)+'\n')








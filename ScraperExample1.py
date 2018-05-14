# -*- coding: utf-8 -*-
import scrapy
import os
import time
import pandas as pd
#read the links stored in the csv file
df=pd.read_csv("jockeylink.csv",header=None)

class JockeyItem(scrapy.Item):
    #Enter all the jockey details you want to collect
    jockeyid=scrapy.Field()
    jockeyname=scrapy.Field()
    season=scrapy.Field()
    stakeswon=scrapy.Field()
    nationality=scrapy.Field()
    ##And all the other fields you may wish to add


class JockeybotSpider(scrapy.Spider):
    name = 'jockeybot'
    allowed_domains = ['#Enter domain here#']
    list_urls = df[1].tolist()
    start_urls = list_urls
    custom_settings = {'FEED_EXPORT_FIELDS': ["jockeyid", "season","jockeyname", "stakeswon",
                                              "nationality","winspast10","wins",
                                              "seconds","thirds","fourths","totalrides",
                                              "winper"]}

    def parse(self, response):

        item=JockeyItem()
        tbls=response.css("table.bigborder")
        trrows=tbls[1].css("tr")

        #jockey data

        str1=response.url
        item['jockeyid']=str1.split("=")[1] #getting the jockey id from url
        item['season']=str1.split("=")[2] ##getting the season from url

        #examining jockey details table to extract information
        #few fields given below
        item['jockeyname']=response.css("td.JTheader::text").extract_first()
        #row data
        tdiv=trrows[2].css("td")
        item['nationality']=tdiv[1].css("::text").extract_first()
        item['wins']=tdiv[3].css("::text").extract_first()
        #nextrow
        tdiv=trrows[3].css("td")
        item['stakeswon']=tdiv[1].css("::text").extract_first().strip()

        yield item
        time.sleep(3)

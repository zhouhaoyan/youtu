# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from youtu.items import YoutuItemLoader, YoutuQuesiontItem, YoutuAnswerItem
from urllib import parse
from youtu.utils.common import get_md5
import datetime
import  re

def handle_strip(value):
    value.replace("\n", "")
    value = value.strip()
    return value


def handle_answer(value):
    if value:
        return value

class YoutuSpider(CrawlSpider):
    name = 'youtu'
    allowed_domains = ['www.ccutu.com']
    start_urls = ['http://www.ccutu.com/wenwen']

    rules = (
        Rule(LinkExtractor(allow=r'wenwen/answer\d+.html'), callback='parse_qa', follow=True),
        Rule(LinkExtractor(allow=r'wenwen/\d+'), follow=True),
    )

    def parse_qa(self, response):
        quesiont_item_loader = YoutuItemLoader(item=YoutuQuesiontItem(), response=response)

        quesiont_item_loader.add_value("url", response.url)
        quesiont_item_loader.add_value("url_object_id", get_md5(response.url))
        quesiont_item_loader.add_css("title", ".wenda_cont .con_left h1::text")
        # quesiont_item_loader.add_css("question", 'meta[name="description"]::attr(content)')
        quesiont_item_loader.add_xpath("question","/html/head/meta[3]")
        quesiont_item_loader.add_css("create_time", ".c_dl_span::text")
        question_item = quesiont_item_loader.load_item()

        answer_list=response.css(".wenda_cont ul li p::text").extract()
        for answer in answer_list:
           answer=handle_strip(answer)
           if handle_answer(answer):
               answer_itme_loader = YoutuItemLoader(item=YoutuAnswerItem(), response=response)
               answer_itme_loader.add_value("answer", answer)
               answer_itme_loader.add_value("url_object_id", get_md5(response.url))
               answer_itme = answer_itme_loader.load_item()

       # yield question_item, answer_itme
        return  question_item,answer_itme

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime, time
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from youtu.settings import SQL_DATETIME_FORMAT, SQL_DATETIME_FORMAT
from w3lib.html import remove_tags


def handle_strip(value):
    value.replace("\n", "")
    value = value.strip()
    return value


class YoutuQuesiontItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field(
        input_processor=MapCompose(handle_strip)
    )
    question = scrapy.Field(
        input_processor=MapCompose(handle_strip)
    )
    create_time = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        now_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        # create_time = datetime.datetime.fromtimestamp(self["create_time"])
        create_time = time.strptime(self["create_time"], "%Y/%m/%d %H:%M:%S")
        create_time = time.strftime(SQL_DATETIME_FORMAT, create_time)
        if self["question"]:
            insert_sql = """
               insert into youtu_question(url_object_id , url, title, question , create_time ,crawl_time,crawl_update_time)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)
                  ON DUPLICATE KEY UPDATE crawl_update_time=VALUES(crawl_update_time)
             """
        else:
            insert_sql = """
                      insert into youtu_question(url_object_id , url, title, question , create_time ,crawl_time,crawl_update_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                         ON DUPLICATE KEY UPDATE crawl_update_time=VALUES(crawl_update_time)
                    """

        params = (self["url_object_id"], self["url"], self["title"], self["title"], create_time,
                  now_time, now_time)
        return insert_sql, params


class YoutuItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class YoutuAnswerItem(scrapy.Item):
    answer = scrapy.Field(
    )
    url_object_id = scrapy.Field()
    create_time = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        now_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        insert_sql = """
               insert into youtu_answer(answer,url_object_id ,crawl_time,crawl_update_time)
                 VALUES (%s, %s, %s, %s)
             """

        params = (self["answer"], self["url_object_id"],
                  now_time, now_time)
        return insert_sql, params

# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import  sys
import  os
#获取绝对路径的 父目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","youtu"])

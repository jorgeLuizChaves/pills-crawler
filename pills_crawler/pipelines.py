# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from twisted.internet import threads


class PillsCrawlerPipeline(object):
    def process_item(self, item, spider):
        def handle_error(item):
            raise DropItem("error processing %s", item)

        d = self.sem.run(threads.deferToThread, self.do_cpu_intense_work, item)
        d.addCallback(lambda _: item)
        d.addErrback(lambda _: handle_error(item))
        return d

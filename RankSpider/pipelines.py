# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import scrapy

from scarpySpider import settings

dbuser = settings.MYSQL_USER
dbpass = settings.MYSQL_PASSWD
dbname = settings.MYSQL_DBNAME
dbhost = settings.MYSQL_HOST
dbport = settings.MYSQL_PORT

class RankPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser,passwd=dbpass,db=dbname,host=dbhost,port=dbport,charset="utf8")
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            print item['rank']
            print item['keyword'].encode('utf-8')
            #INSERT
            #INTO
            #zzcms_seo_costdetail(platformid, keywordid, webid, userid, createtime, rank, priceone, pricetwo)
            #VALUES()
            if int(item['rank']) <= 10:
                print item['rank']
                priceone = item['priceone']
                pricetwo = 0
            elif int(item['rank']) <=20:
                print item['rank']
                priceone = 0
                pricetwo = item['pricetwo']
            else:
                priceone = 0
                pricetwo = 0
            self.cursor.execute("""INSERT INTO zzcms_seo_costdetail(platformid,keywordid,webid,userid,createTime,rank,priceone,pricetwo,keywordname)
                                       VALUES (%s,%s, %s, %s, now(),%s,%s,%s,%s)""",
                                (
                                    item['platformId'],
                                    item['keywordId'],
                                    item['webId'],
                                    item['userId'],
                                    item['rank'],
                                    priceone,
                                    pricetwo,
                                    item['keyword'].encode('utf-8')
                                )
                                )
            print '-------------------test--------------------'
            self.conn.commit()


        except MySQLdb.Error,e:
            print "Error %d:%s" % (e.args[0],e.args[1])
        return item

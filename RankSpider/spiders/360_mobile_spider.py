#-*-coding:utf-8-*-
import scrapy
import urllib
import re
import json
import MySQLdb
from urllib import quote_plus

from scarpySpider.spiders import html_downloader
from scarpySpider.spiders import html_parser

from scarpySpider.items import ScarpyspiderItem

from scarpySpider import  settings

dbuser = settings.MYSQL_USER
dbpass = settings.MYSQL_PASSWD
dbname = settings.MYSQL_DBNAME
dbhost = settings.MYSQL_HOST
dbport = settings.MYSQL_PORT

class QuotesSpider(scrapy.Spider):
    name = "360_mobile_rank"

    def __init__(self):
        # self.keyword = keyword_manager.KeywordManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        # self.outputer = html_outputer.HtmlOutputer()
        self.conn = MySQLdb.connect(user=dbuser, passwd=dbpass, db=dbname, host=dbhost, port=dbport, charset="utf8")
        self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.conn.commit()

    def start_requests(self):
        # urls = {
        #     'http://quotes.toscrape.com/page/1/',
        #     'http://quotes.toscrape.com/page/2/',
        # }
        # SELECT * FROM zzcms_admin a LEFT JOIN zzcms_seo_keyword b ON a.id=b.`userid` WHERE b.platformid=1 GROUP BY b.name
        self.cursor.execute("SELECT a.id,c.id as webid,b.priceone as priceone,b.pricetwo as pricetwo,b.id as keywordid,a.`username`,b.platformid,b.name as keywordname,c.websiteurl "
                            "FROM zzcms_admin a "
                            "LEFT JOIN zzcms_seo_keyword b "
                            "ON a.id=b.`userid` "
                            "LEFT JOIN zzcms_seo_web c "
                            "ON a.id=c.`userid` "
                            "WHERE b.platformid=7 and a.balance>0 "
                            "GROUP BY c.id,b.name")
        self.cursor.scroll(0,"absolute")
        header = {
            "Host": "m.so.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}
        for line in self.cursor.fetchall():
            user_id = line["id"]
            webid=line["webid"]
            #root_name = line["companyKeyword"].encode("utf-8").split(",")
            keyword = line['keywordname'].encode("utf-8")
            keywordid = line['keywordid']
            priceone = line['priceone']
            pricetwo = line['pricetwo']
            root_user_url = line["websiteurl"]
            root_url = "https://m.so.com/s"
            pn = 1
            keyword_t = quote_plus(keyword)
            first_url = "%s?q=%s&pn=%d" % (root_url,keyword_t,pn)
            yield scrapy.Request(url=first_url,headers=header, dont_filter=True, meta={'page_n':pn,'root_url':root_url,'keywordid':keywordid,'user_id':user_id,'webid':webid,'priceone':priceone,'pricetwo':pricetwo,'root_name_all':keyword,'root_user_url':root_user_url},callback=self.parse)

        self.cursor.close()

    def parse(self, response):
        # print response.body
        # page = response.url.split("/")[-2]

        page = response.body
        new_data = self.parser.sou_360_mobile_paser(page)

        item = ScarpyspiderItem()
        item['userId'] = response.meta['user_id']
        item['platformId'] = '7'
        item['webId'] = response.meta['webid']
        item['keywordId'] = response.meta['keywordid']
        item['priceone'] = response.meta['priceone']
        item['pricetwo'] = response.meta['pricetwo']

        root_name_single = response.meta['root_name_all']
        root_name = quote_plus(root_name_single)

        root_pn = response.meta['page_n']
        domain_rank = -1

        # 得到客户的域名地址
        user_url_data = response.meta['root_user_url'].split(".")
        leng_url = len(user_url_data)
        if leng_url == 1:
            user_domain = user_url_data
        elif leng_url > 1:
            user_domain = response.meta['root_user_url']
        else:
            user_domain = '请输入域名'

        for name in new_data:
            pattern = re.compile(r'%s' % user_domain)
            result1 = re.search(pattern, name.get_text())
            if result1:
                domain_rank = new_data.index(name) + 1
                domain_rank = (root_pn-1)*10 + domain_rank
                item['rank'] = str(domain_rank)
                # print root_name_single
                item['keyword'] = root_name_single.decode('utf-8')
                # print item['keyword'].encode('utf-8')
                # print  '%s %s %s' %(item['rank'],item['keyword'],item['platformId'])
                # print domain_rank
                yield item
                break

        root_pn = root_pn + 1
        if domain_rank == -1 and root_pn != 6:
            root_url = response.meta['root_url']
            keywordid = response.meta['keywordid']
            user_id = response.meta['user_id']
            webid = response.meta['webid']
            priceone = response.meta['priceone']
            pricetwo = response.meta['pricetwo']
            keyword = response.meta['root_name_all']
            root_user_url = response.meta['root_user_url']
            html_wd_pn = "?q=%s&pn=%d" % (root_name, root_pn)
            first_url = response.meta['root_url'] + html_wd_pn
            header = {
                "Host": "m.so.com",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}
            yield scrapy.Request(url=first_url,headers=header, meta={'page_n': root_pn, 'root_url': root_url, 'keywordid': keywordid,
                                                      'user_id': user_id, 'webid': webid, 'priceone': priceone,
                                                      'pricetwo': pricetwo, 'root_name_all': keyword,
                                                      'root_user_url': root_user_url}, callback=self.parse)

        if domain_rank == -1 and root_pn == 6:
            item['rank'] = '100'
            # print root_name_single
            item['keyword'] = root_name_single.decode('utf-8')
            # print item['keyword'].encode('utf-8')
            # print  '%s %s %s' %(item['rank'],item['keyword'],item['platformId'])
            yield item
            # print item['rank']

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
    name = "sogou_mobile_rank"

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
                            "WHERE b.platformid=4 and a.balance>0 "
                            "GROUP BY c.id,b.name")
        self.cursor.scroll(0,"absolute")
        header = {
            "Host": "m.sogou.com",
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
            root_url = "https://m.sogou.com/web/searchList.jsp"
            keyword_t = quote_plus(keyword)
            first_url = "%s?keyword=%s" % (root_url,keyword_t)
            yield scrapy.Request(url=first_url, dont_filter=True,headers=header, meta={'root_url':root_url,'keywordid':keywordid,'user_id':user_id,'webid':webid,'priceone':priceone,'pricetwo':pricetwo,'root_name_all':keyword,'root_user_url':root_user_url},callback=self.parse)
            #for keyword in root_name:
            #    keyword_t = quote_plus(keyword)
            #    first_url = "%s?wd=%s&pn=0" % (root_url,keyword_t)
            #    yield scrapy.Request(url=first_url, meta={'root_url':root_url,'company_id':company_id,'root_name':root_name,'root_name_all':keyword,'root_user_url':root_user_url},callback=self.parse)

        self.cursor.close()

        # root_name = ['长沙平江香干']
        # root_name = root_name.encode('utf-8')
        # root_user_url = 'www.djpjxg.com'
        # root_user_url = 'http://www.seoai.cn/'
        # print root_name
        # root_pn = 0
        # for url in urls:

    def parse(self, response):
        # print response.body
        # page = response.url.split("/")[-2]

        page = response.body
        new_data = self.parser.sougou_mobile_paser(page)

        item = ScarpyspiderItem()
        item['userId'] = response.meta['user_id']
        item['platformId'] = '4'
        item['webId'] = response.meta['webid']
        item['keywordId'] = response.meta['keywordid']
        item['priceone'] = response.meta['priceone']
        item['pricetwo'] = response.meta['pricetwo']

        root_name_single = response.meta['root_name_all']
        root_name = quote_plus(root_name_single)

        root_pn = 1
        domain_rank = (root_pn-1) * 10 - 1

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
                break

        if domain_rank == -1:
            item['rank'] = '100'
                    # print root_name_single
            item['keyword'] = root_name_single.decode('utf-8')
                    # print item['keyword'].encode('utf-8')
                    # print  '%s %s %s' %(item['rank'],item['keyword'],item['platformId'])
                # break

            # print item['rank']
        return item

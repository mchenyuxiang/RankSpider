#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import re
import urllib

class HtmlParser(object):

    def _baidu_get_urls(self,soup):
        new_urls = set()
        links = soup.find_all(['a','span'],class_='c-showurl')
        return links

    # 百度列表网页解析
    def baidu_paser(self,html_cont):
        if html_cont is None:
            return

        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls = self._baidu_get_urls(soup)
        return new_urls

    # 百度列表网页解析
    def _baidu_mobile_get_urls(self,soup):
        new_urls = set()
        links = soup.find_all(['span'],class_='c-showurl')
        return links

    def baidu_mobile_paser(self,html_cont):
        if html_cont is None:
            return

        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls = self._baidu_mobile_get_urls(soup)
        return new_urls

    # 搜狗列表网页解析
    def _sougou_get_urls(self,soup):
        new_urls = set()
        # links = soup.findAll('cite')
        links = soup.find_all(['cite'],attrs={'id':re.compile('cacheresult_info_*')})
        return links

    def sougou_paser(self,html_cont):
        if html_cont is None:
            return

        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls = self._sougou_get_urls(soup)
        return new_urls

    # 360列表网页解析
    def _sou_360_get_urls(self,soup):
        new_urls = set()
        # links = soup.findAll('cite')
        links = soup.find_all(['p'],class_="res-linkinfo")
        # links = soup.find_all(['cite'],attrs={'id':re.compile('cacheresult_info_[0-9]]')})
        return links

    def sou_360_paser(self,html_cont):
        if html_cont is None:
            return

        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls = self._sou_360_get_urls(soup)
        return new_urls
    # 360列表网页解析
    def _sou_360_mobile_get_urls(self,soup):
        new_urls = set()
        # links = soup.findAll('cite')
        links = soup.find_all(['cite'],class_="res-show-url")
        # links = soup.find_all(['cite'],attrs={'id':re.compile('cacheresult_info_[0-9]]')})
        return links

    def sou_360_mobile_paser(self,html_cont):
        if html_cont is None:
            return

        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls = self._sou_360_mobile_get_urls(soup)
        return new_urls
    # sougou mobile列表网页解析
    def _sougou_mobile_get_urls(self,soup):
        new_urls = set()
        # links = soup.findAll('cite')
        links = soup.find_all(['div'],class_="citeurl")
        # links = soup.find_all(['cite'],attrs={'id':re.compile('cacheresult_info_[0-9]]')})
        return links

    def sougou_mobile_paser(self,html_cont):
        if html_cont is None:
            return

        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls = self._sougou_mobile_get_urls(soup)
        return new_urls

    # shenma列表网页解析
    def _shenma_get_urls(self,soup):
        new_urls = set()
        # links = soup.findAll('span')
        links = soup.find_all(['div'],class_="other")
        # links = soup.find_all(['cite'],attrs={'id':re.compile('cacheresult_info_[0-9]]')})
        return links

    def shenma_paser(self,html_cont):
        if html_cont is None:
            return

        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls = self._shenma_get_urls(soup)
        return new_urls

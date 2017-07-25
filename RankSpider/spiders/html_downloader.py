#-*-coding:utf-8-*-
import urllib
import urllib2

class HtmlDownloader(object):
    def download(self,url):
        if url is None:
            return None
        # response1 = urllib.urlopen(url)

        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
        response = urllib2.urlopen(request)

        if response.getcode() != 200:
            return None

        return  response.read()

    def mobile_download(self,url):
        if url is None:
            return None
        # response1 = urllib.urlopen(url)

        request = urllib2.Request(url)
        request.add_header('User-Agent',"Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1")
        response = urllib2.urlopen(request)

        if response.getcode() != 200:
            return None

        return response.read()
# coding=UTF-8
# 下载器

import urllib2

class HtmlDownloader(object):

    def download(self, new_url):
        if new_url is None:
            print 'download new_url为空'
            return None

        response = urllib2.urlopen(new_url)
        if response.getcode() != 200:
            print 'download getcode不是200'
            return None
        else:
            return response.read()
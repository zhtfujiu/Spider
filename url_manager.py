# coding=UTF-8
# URL 管理器


import Queue

class UrlManager(object):

    def __init__(self):
        self.new_urls = Queue.Queue()
        self.old_urls = Queue.Queue()

    def add_new_url(self, new_url):
        if new_url is None: # 如果是空，直接退出
            print 'add_new_url  new_url为空'
            return
        # if new_url not in self.new_urls and new_url not in self.old_urls: # 既不在旧的也不在新的，可添加
        self.new_urls.put(new_url)


    def add_new_urls(self, new_urls):
        # print '原有的URL数量为：', len(self.new_urls)
        if new_urls is None or new_urls.empty() : # 判断是否为空，是否长度为0
            print 'add_new_urls  new_urls为空'
            return
        # for new_url in new_urls: # 调用上一个单个添加的方法来做
        while not new_urls.empty():
            self.add_new_url(new_urls.get())
        # print 'new_url添加完毕'

    def get_new_url(self): #获取顶部的URL
        new_url = self.new_urls.get() # pop会弹出，导致原urls里少一个
        self.old_urls.put(new_url) # 添加进old里
        return new_url

    def has_new_url(self):
        return not self.new_urls.empty() # 如果待爬取列表不为0，则证明有有待爬取的
# coding=UTF-8
# 对百度百科Python词条及其1000个相关页面的词条及摘要数据进行爬取
# 爬虫入口
import wx

import html_downloader
import html_outputer
import html_parser
import url_manager


class Doing_Spider(object):

    def __init__(self, parent, driver, entry, num, status_text):
        self.parent = parent
        self.entry = entry
        self.num = num
        self.driver = driver
        self.status_text = status_text

        self.urls = url_manager.UrlManager()

        # =========准备多线程  3个线程  3个URL管理器  3个downloader  ========
        self.urls_1 = url_manager.UrlManager()
        self.urls_2 = url_manager.UrlManager()
        self.urls_3 = url_manager.UrlManager()

        self.downloader_1 = html_downloader.HtmlDownloader()
        self.downloader_2 = html_downloader.HtmlDownloader()
        self.downloader_3 = html_downloader.HtmlDownloader()


        self.downloader = html_downloader.HtmlDownloader()
        self.outputer = html_outputer.HtmlOutputer()
        self.parser = html_parser.HtmlParser()

    def crawl(self):
        driver = self.driver

        self.parent.status_text.SetLabel('')
        self.parent.status_text.Update()

        spider_url = 'https://baike.baidu.com/'

        while True:
            if driver.current_url != spider_url:
                driver.get(spider_url)

            entry = self.entry
            # 锁定页面的输入框，将用户词条输入
            driver.find_element_by_id("query").send_keys(entry)  # 注意汉语编码
            # 搜索   这里需要加一个对搜索结果的检测，该词条是否存在!!!!!!
            driver.find_element_by_id("search").click()
            # 搜索不到词条的话，都是下面这中url，后期匹配一下
            # http://baike.baidu.com/search/none?word=wowowow&pn=0&rn=10&enc=utf8
            if 'item' in driver.current_url and 'search/none' not in driver.current_url:
                # 搜索有结果,进行下一步爬取工作

                num = self.num

                print entry, num

                num = int(num)  #转变为int整型
                count = 1  # 变量count记录当前爬取的是第几个URL


                # =============这一片段内是爬取过程，等会拆分为一个线程操作 =========

                self.urls.add_new_url(driver.current_url)  # 添加根URL

                while self.urls.has_new_url():  # 爬虫的循环
                    # 异常处理，避免无效URL带来的崩溃
                    try:
                        new_url = self.urls.get_new_url()  # 获取一个待爬取的URL，添加进URL管理器
                        now_text =  u'%s : %s' % (count,new_url)
                        print now_text
                        # 把现在的信息添加在展示栏
                        self.parent.status_text.AppendText(now_text+"\n")
                        self.parent.status_text.ShowPosition(self.parent.status_text.GetLastPosition())
                        # self.parent.status_text.Update()
                        self.parent.status_text.Refresh()

                        html_content = self.downloader.download(new_url)  # 启动下载器，存储进html_content里
                        new_urls, new_data = self.parser.parse(new_url, html_content)  # 解析器对该URL的内容进行解析，分离出新的URL和数据
                        self.urls.add_new_urls(new_urls)  # 批量添加URL，跟上面那个add_new_url不一样，那个是单独添加一条
                        self.outputer.collect_data(new_data)  # 对数据进行收集

                        # 自定爬取数目
                        if count == num:
                            print num, '条数据已爬取完成'
                            break
                        count = count + 1
                    except:
                        print '本条爬取失败'
                        self.parent.status_text.AppendText(u'本条爬取失败')
                        self.parent.status_text.Update()

                # ==========上面这一片段内是爬取过程，等会拆分为一个线程操作 ==========

                # ========== 存储之前要把三个URL管理器的合并进一个总的URL管理器 =======




                # ========== 存储之前要把三个URL管理器的合并进一个总的URL管理器 =======


                try:
                    self.outputer.output_mysql()
                    print '数据已存储至数据库'
                    self.parent.status_text.AppendText(u'数据已存储至数据库')
                    self.parent.status_text.Refresh()

                    # dlg = wx.MessageDialog(None, '词条信息爬取完毕，并保存至数据库相应的数据表中。', '爬取成功！', wx.OK)
                    # if dlg.ShowModal() == wx.ID_OK:
                    #     dlg.Destroy()

                except Exception, e:
                    print '存储过程错误：', e
                    self.parent.status_text.AppendText(u'存储过程错误')
                    self.parent.status_text.Refresh()
                break
            else:
                dlg = wx.MessageDialog(None, entry.encode('utf-8') + '词条不存在', '词条不存在', wx.OK)
                if dlg.ShowModal() == wx.ID_OK:
                    dlg.Destroy()
                break
                print '您输入的词条不存在，请重新输入'

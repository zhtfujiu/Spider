# coding=UTF-8
import wx

from doing_spider import Doing_Spider


class GUI_SPIDER(wx.Frame):
    def __init__(self, parent):
        super(GUI_SPIDER, self).__init__(parent, title="爬取百科词条", size=(500, 300))
        self.parent = parent
        self.Bind(wx.EVT_CLOSE, self.frameClose)  # 对系统进行监听关闭键
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        # 最外层盒子，垂直方向
        self.boxsizer = wx.BoxSizer(wx.VERTICAL)

        # 第1个内层盒子，内建两个盒子，用户名和密码
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # 水平 一个提示语 一个输入框
        hbox1_1 = wx.BoxSizer(wx.HORIZONTAL)
        static_str1 = wx.StaticText(panel, label='启动词条：')
        hbox1_1.Add(static_str1, flag=wx.ALIGN_CENTER_VERTICAL, border=10)
        self.entry_blank = wx.TextCtrl(panel)
        hbox1_1.Add(self.entry_blank)

        hbox1.Add(hbox1_1,proportion=1)

        # 水平 一个提示语 一个输入框
        hbox1_2 = wx.BoxSizer(wx.HORIZONTAL)
        static_str2 = wx.StaticText(panel, label='爬取数量：')
        hbox1_2.Add(static_str2, flag=wx.ALIGN_CENTER_VERTICAL, border=10)
        self.num_blank = wx.TextCtrl(panel)
        hbox1_2.Add(self.num_blank)

        hbox1.Add(hbox1_2, proportion=1)

        # 最外层盒子添加内层1号盒子
        self.boxsizer.Add(hbox1, flag=wx.ALIGN_CENTER | wx.TOP | wx.ALIGN_CENTER_VERTICAL, border=10)
        # 下边距10
        # self.boxsizer.Add((-1, 10))

        # ================ 2号区域，直接放Text展示框，爬虫状态提示===========
        self.status_text = wx.TextCtrl(panel, style=wx.TE_READONLY)  # 只读模式 |
        self.boxsizer.Add(self.status_text, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)


        # 创建内层3号盒子，内含两个按钮，水平放置
        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        # 按钮大小，名称设置
        btn_back = wx.Button(panel, label='返回上层菜单', size=(120, 30))
        btn_back.Bind(wx.EVT_LEFT_DOWN, self.back2home)
        self.hbox3.Add(btn_back)
        btn_spider = wx.Button(panel, label='启动爬虫', size=(120, 30))
        self.hbox3.Add(btn_spider, flag=wx.LEFT | wx.BOTTOM, border=5)  # 按钮距离左侧和底部都是5
        btn_spider.Bind(wx.EVT_LEFT_DOWN, self.startSpider)
        # 最外层盒子添加内层4号盒子，盒子右对齐，靠在外层盒子的右侧，边距10
        self.boxsizer.Add(self.hbox3, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        panel.SetSizer(self.boxsizer)

    def back2home(self, event):
        self.parent.Show()
        self.Destroy()
        event.Skip()

    def frameClose(self, event):
        # 监听系统的关闭键
        self.parent.Show()
        event.Skip()

    def startSpider(self, event):
        # 启动爬虫
        entry = self.entry_blank.GetLineText(0)
        num = self.num_blank.GetLineText(0)

        doing_spider = Doing_Spider(self, self.parent.driver, entry, num, self.status_text)
        doing_spider.crawl()

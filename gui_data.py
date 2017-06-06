# coding=UTF-8
import wx
import wx.grid

from doing_mysql import Doing_mysql


class GUI_DATA(wx.Frame):
    def __init__(self, parent):
        super(GUI_DATA, self).__init__(parent, title="数据分析系统", size=(1200, 800))
        self.parent = parent
        self.doing_mysql = Doing_mysql()
        self.Bind(wx.EVT_CLOSE, self.frameClose)  # 对系统进行监听关闭键
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        # 最外层盒子，垂直方向
        self.boxsizer = wx.BoxSizer(wx.VERTICAL)

        # 第1个内层盒子，内建两个盒子,一左一右
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # 左侧细长的盒子，垂直
        hbox1_1 = wx.BoxSizer(wx.VERTICAL)

        # ==============左侧第三个功能=========

        hbox1_1_3 = wx.BoxSizer(wx.HORIZONTAL)
        static_str3 = wx.StaticText(panel, label='预览词条文件：')
        hbox1_1_3.Add(static_str3, flag=wx.ALIGN_CENTER_VERTICAL)
        self.entry_view_blank = wx.TextCtrl(panel)  # , size=(200,20))
        hbox1_1_3.Add(self.entry_view_blank, flag=wx.ALIGN_CENTER_VERTICAL)

        hbox1_1.Add(hbox1_1_3, flag=wx.ALL, border=15)

        btn_view = wx.Button(panel, label='获取预览信息', size=(120, 30))
        btn_view.Bind(wx.EVT_LEFT_DOWN, self.getview)  # 监听事件，获取预览信息
        hbox1_1.Add(btn_view, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)
        hbox1_1.Add((-1, 5))

        btn_empty = wx.Button(panel, label='清空预览信息', size=(120, 30))
        btn_empty.Bind(wx.EVT_LEFT_DOWN, self.emptyview)  # 监听事件，清空预览信息
        hbox1_1.Add(btn_empty, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)
        hbox1_1.Add((-1, 25))

        # =============左侧第一个功能==========
        hbox1_1_1 = wx.BoxSizer(wx.HORIZONTAL)
        static_str1 = wx.StaticText(panel, label='要导出Excel文件的根词条：')
        hbox1_1_1.Add(static_str1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.entry_blank = wx.TextCtrl(panel)#, size=(200,20))
        hbox1_1_1.Add(self.entry_blank, flag=wx.ALIGN_CENTER_VERTICAL)

        hbox1_1.Add(hbox1_1_1, flag=wx.ALL, border=15)

        btn_export = wx.Button(panel, label='导出Excel', size=(120,30))
        btn_export.Bind(wx.EVT_LEFT_DOWN, self.export2Excel)  # 监听事件，导出Excel
        hbox1_1.Add(btn_export, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)
        hbox1_1.Add((-1,25))
        # ==============左侧第二个功能==========

        hbox1_1_2 = wx.BoxSizer(wx.VERTICAL)
        static_str2 = wx.StaticText(panel, label='【开发者选项】 慎选！\n请按语法规定输入SQL语句：')
        hbox1_1_2.Add(static_str2, flag=wx.EXPAND | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        self.sql_blank = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(240, 100))  # , size=(200,20))
        hbox1_1_2.Add(self.sql_blank, flag=wx.EXPAND | wx.TOP, border=15)

        hbox1_1.Add(hbox1_1_2, flag=wx.ALL, border=15)

        btn_dosql = wx.Button(panel, label='执行SQL语句', size=(120, 30))
        btn_dosql.Bind(wx.EVT_LEFT_DOWN, self.doSQL)  # 监听事件，执行SQL语句
        hbox1_1.Add(btn_dosql, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)


        # ===============右侧大表==============
        hbox1.Add(hbox1_1, proportion=2)


        # 右侧宽大的，直接用GridSizer放进Box
        hbox1_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.grid = wx.grid.Grid(panel)
        self.grid.CreateGrid(100, 10)  # 100行10列
        # self.grid.SetCellValue(0,0,'hello')


        hbox1_2.Add(self.grid, flag=wx.ALIGN_RIGHT, border=35)
        hbox1.Add(hbox1_2, proportion=2)


        # 最外层盒子添加内层1号盒子
        self.boxsizer.Add(hbox1, flag= wx.TOP | wx.ALIGN_CENTER_VERTICAL, proportion=15, border=10)
        # 下边距10
        self.boxsizer.Add((-1, 10))

        # ==============底部按钮==============
        # 创建内层3号盒子，内含两个按钮，水平放置
        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        # 按钮大小，名称设置
        btn_back = wx.Button(panel, label='返回上层菜单', size=(120, 30))
        btn_back.Bind(wx.EVT_LEFT_DOWN, self.back2home)
        self.hbox3.Add(btn_back)
        btn_exit = wx.Button(panel, label='退出系统', size=(120, 30))
        self.hbox3.Add(btn_exit, flag=wx.LEFT | wx.BOTTOM, border=5)  # 按钮距离左侧和底部都是5
        btn_exit.Bind(wx.EVT_LEFT_DOWN, self.closeFrame)

        # 最外层盒子添加内层4号盒子，盒子右对齐，靠在外层盒子的右侧，边距10
        self.boxsizer.Add(self.hbox3, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        panel.SetSizer(self.boxsizer)

    def back2home(self, event):
        self.doing_mysql.do_end_sql()
        self.parent.Show()
        self.Destroy()
        # self.Hide()
        event.Skip()

    def frameClose(self, event):
        # 监听系统的关闭键
        self.parent.Show()
        self.doing_mysql.do_end_sql()
        event.Skip()

    def export2Excel(self, event):
        # 导出Excel文件
        tablename = self.entry_blank.GetLineText(0)

        if self.doing_mysql.do_check_is_in(tablename):
            # 返回真证明不存在, 弹框提示
            dlg = wx.MessageDialog(None, tablename.encode('utf-8') + '数据表不存在，请核对或导出其他词条文件！', '词条文件不存在！', wx.OK)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Destroy()

        else:
            # 返回假证明存在, 执行导出操作
            if self.doing_mysql.do_ecport2excel(tablename):
                # 导出成功
                dlg = wx.MessageDialog(None, tablename.encode('utf-8') + '.xlsx文件导出成功，请前往桌面查看！', '导出成功！', wx.OK)
                if dlg.ShowModal() == wx.ID_OK:
                    dlg.Destroy()
                    self.entry_blank.Clear()
            else:
                # 导出失败
                dlg = wx.MessageDialog(None, tablename.encode('utf-8') + '.xlsx文件导出失败，请重新尝试导出！', '导出失败！', wx.OK)
                if dlg.ShowModal() == wx.ID_OK:
                    dlg.Destroy()

        event.Skip()

    def getview(self, event):
        entry = self.entry_view_blank.GetLineText(0)
        if self.doing_mysql.do_check_is_in(entry):
            # 返回真证明不存在, 弹框提示
            dlg = wx.MessageDialog(None, entry.encode('utf-8') + '数据表不存在，请核对或导出其他词条文件！', '词条文件不存在！', wx.OK)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Destroy()
        else:
            self.doing_mysql.do_getdata2grid(entry, self.grid)
            self.grid.Update()

        event.Skip()

    def emptyview(self, event):
        self.grid.ClearGrid()
        self.entry_view_blank.Clear()
        event.Skip()


    def doSQL(self, event):
        # 执行SQL语句
        self.grid.ClearGrid()
        sql = self.sql_blank.GetValue()
        # print sql
        if self.doing_mysql.do_DIYsql2grid(sql, self.grid):
            pass
        else:
            dlg = wx.MessageDialog(None, 'SQL执行失败，请仔细核对是否为语法问题！', '执行失败！', wx.OK)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Destroy()
        event.Skip()

    def closeFrame(self, event):
        # 关闭整个系统
        self.doing_mysql.do_end_sql()
        self.parent.Close()
        self.Destroy()
        event.Skip()
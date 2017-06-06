# coding=UTF-8
import wx
from doing_mysql import Doing_mysql

from doing_auto_login import Doing_Auto_login


class GUI_LOGIN(wx.Frame):
    def __init__(self, parent):
        super(GUI_LOGIN, self).__init__(parent, title="登录", size=(500, 300))
        self.parent = parent  # 尝试用这个回到原界面
        self.Bind(wx.EVT_CLOSE, self.frameClose)  # 对系统进行监听关闭键
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        # 最外层盒子，垂直方向
        self.boxsizer = wx.BoxSizer(wx.VERTICAL)

        # 第1个内层盒子，内建两个盒子，用户名和密码
        hbox1 = wx.BoxSizer(wx.VERTICAL)

        # 水平 一个提示语 一个输入框
        hbox1_1 = wx.BoxSizer(wx.HORIZONTAL)
        static_str1 = wx.StaticText(panel, label='账户：')  #, flag=wx.RIGHT, border=10)
        hbox1_1.Add(static_str1, flag=wx.ALIGN_CENTER_VERTICAL, border=15)
        self.username_blank = wx.TextCtrl(panel, size=(270, 30))  # 用户名输入框
        hbox1_1.Add(self.username_blank)

        hbox1.Add(hbox1_1, flag=wx.BOTTOM, border=20)

        # 水平 一个提示语 一个输入框
        hbox1_2 = wx.BoxSizer(wx.HORIZONTAL)
        static_str2 = wx.StaticText(panel, label='密码：')  # , flag=wx.RIGHT, border=10)
        hbox1_2.Add(static_str2, flag=wx.ALIGN_CENTER_VERTICAL, border=15)
        self.psw_blank = wx.TextCtrl(panel, style=wx.TE_PASSWORD, size=(270, 30))  # 密码输入框
        hbox1_2.Add(self.psw_blank)

        hbox1.Add(hbox1_2, flag=wx.BOTTOM, border=20)

        # 最外层盒子添加内层1号盒子
        self.boxsizer.Add(hbox1, proportion=1, flag=wx.ALIGN_CENTER | wx.TOP | wx.ALIGN_CENTER_VERTICAL, border=60)
        # 下边距10
        self.boxsizer.Add((-1, 10))



        # 创建内层2号盒子，内含两个按钮，水平放置
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # 按钮大小，名称设置
        btn_back = wx.Button(panel, label='返回上层菜单', size=(120, 30))
        # 绑定事件
        btn_back.Bind(wx.EVT_LEFT_DOWN, self.back2home)
        self.hbox2.Add(btn_back)
        btn_login = wx.Button(panel, label='登录爬取个人信息', size=(120, 30))
        self.hbox2.Add(btn_login, flag=wx.LEFT | wx.BOTTOM, border=5)  # 按钮距离左侧和底部都是5
        btn_login.Bind(wx.EVT_LEFT_DOWN, self.login)  # 绑定登录监听

        # 最外层盒子添加内层4号盒子，盒子右对齐，靠在外层盒子的右侧，边距10
        self.boxsizer.Add(self.hbox2, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        panel.SetSizer(self.boxsizer)

    def back2home(self, event):
        self.parent.Show()
        self.Destroy()
        event.Skip()

    def frameClose(self, event):
        # 监听系统的关闭键
        self.parent.Show()
        event.Skip()

    def login(self,event):
        # 原线程
        while True:
            username = self.username_blank.GetLineText(0)
            psw = self.psw_blank.GetLineText(0)

            print username, psw
            # 实例化Auto_login_baidu类
            auto_login = Doing_Auto_login(self.parent.driver, username, psw)
            if auto_login.login():
                # 获得TRUE表示登录成功，可以执行爬取信息操作
                # 后续爬取个人信息未完成
                if auto_login.get_user_baike_info():
                    # 爬取成功，弹框提示
                    dlg_1 = wx.MessageDialog(None, '登录成功。个人百科信息爬取成功，是否立即导出Excel文件到本机？',
                                             '爬取成功', wx.YES_NO)
                    if dlg_1.ShowModal() == wx.ID_YES:
                        # 用户要求立即导出Excel文件，执行导出操作。
                        doing_mysql = Doing_mysql()
                        if doing_mysql.do_ecport2excel(auto_login.get_html_username()):
                            # 导出成功
                            dlg_1_1 = wx.MessageDialog(None, '导出成功，请前往桌面查看！', '导出Excel成功', wx.OK)
                            if dlg_1_1.ShowModal() == wx.ID_OK:
                                dlg_1_1.Destroy()
                                doing_mysql.do_end_sql()
                            break  # 成功的完成所有操作，退出至登录界面
                        else:
                            # 导出失败
                            dlg_1_2 = wx.MessageDialog(None, '导出失败！', '错误', wx.OK)
                            if dlg_1_2.ShowModal() == wx.ID_OK:
                                dlg_1_2.Destroy()
                                doing_mysql.do_end_sql()
                            # 导出失败暂时不加循环了，心累！！！！
                            break

                    else:
                        # 用户暂不希望导出，弹框关闭
                        dlg_1.Destroy()
                        break  # 退出循环
                else:
                    # 爬取失败
                    dlg_2 = wx.MessageDialog(None, '登录成功。个人信息爬取失败，请重新登录并爬取。', '爬取失败', wx.OK)
                    if dlg_2.ShowModal() == wx.ID_OK:
                        # 尝试再次爬取
                        print '重新爬取'
                        dlg_2.Destroy()

            else:
                # 登录失败，确认账号密码重新登录
                dlg = wx.MessageDialog(None, '登陆失败，请核对用户名和密码！', '登录失败', wx.OK)
                if dlg.ShowModal() == wx.ID_OK:
                    dlg.Destroy()
                self.username_blank.Clear()
                self.psw_blank.Clear()
                break

        event.Skip()

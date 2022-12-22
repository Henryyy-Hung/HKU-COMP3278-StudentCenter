# -*- coding:utf-8 -*-
from tkinter import *
from tkinter import font as tkFont
from tkinter import ttk
from tkinter.tix import *
from PIL import Image, ImageTk

import cv2
import datetime
import numpy
import os
import sys
import threading
import webbrowser

from controller import *

from loginframe import *
from homeframe import *
from coursesframe import *
from timetableframe import *
from recordsframe import *
from settingframe import *

class ICMSGraphicalUserInterface(object):

    def __init__(self):
        self.controller = Controller()

        ## 定义当前页面
        self.current_page = ""

        ## 构建页面
        self.add_widgets()

        ## 默认无显示
        self.current_frame = Frame(master=self.display_panel)

    def add_widgets(self):
        ## 定义根视窗的长和宽
        self.wh_ratio = 1.8
        self.root_width = 1200
        self.root_height = int(self.root_width/self.wh_ratio)

        ## 设置根视窗外观
        self.root = Tk()
        self.root.title(values.ROOT_TITLE)
        self.root.iconbitmap(self.get_resource_path(f'./{"res"}{os.sep}{"icon"}{os.sep}{"icon.ico"}'))
        self.root.configure(bg=values.ROOT_BG_COLOR)

        ## 定义根视窗位置
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        alignstr = f'{int(self.root_width)}x{int(self.root_height)}+{int((self.screenwidth - self.root_width) / 2)}+{int((self.screenheight - self.root_height) / 2)}'
        self.root.geometry(alignstr)
        self.root.minsize(width=self.root_width, height=self.root_height)

        ## 屏幕太小时全屏
        if (self.screenwidth < 1.2 * self.root_width or self.screenheight < 1.2 * self.root_height):
            self.root.state('zoomed')

        def on_closing():
            if (getattr(self.controller, 'student_id')>0):
                self.post_logout_time()
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)
            
        ## 侧边栏
        self.side_bar = Frame(master=self.root, bg=values.SIDE_BAR_BG_COLOR, width=240)
        self.side_bar.pack(fill=Y, expand=False, side=LEFT)

        ## 主窗口
        self.main_frame = Frame(master=self.root, bg=values.ROOT_BG_COLOR)
        self.main_frame.pack(fill=BOTH, expand=True, side=LEFT)

        ## 按键栏 <- 基于侧边栏
        self.button_panel = Frame(master=self.side_bar, bg=values.SIDE_BAR_BG_COLOR)
        self.button_panel.place(relx=0.5, rely=0.5, width=225, relheight=1, anchor=CENTER)


        ## 主页键 <- 按键栏
        self.img_home = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"home.png"}'))
        self.img_home_hover = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"home_hover.png"}'))
        self.img_home_selected = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"home_selected.png"}'))
        self.button_home = Button(master=self.button_panel, image=self.img_home, bg=values.SIDE_BAR_BG_COLOR, activebackground=values.SIDE_BAR_BG_COLOR, border=0)
        self.button_home.pack(fill=X, expand=False, side=TOP, pady=(30, 5))
        self.button_home.bind('<Enter>', lambda e: self.button_home.configure(image=self.img_home_hover if (self.current_page!="home") else self.img_home_selected))
        self.button_home.bind('<Leave>', lambda e: self.button_home.configure(image=self.img_home if (self.current_page!="home") else self.img_home_selected))
        self.button_home.configure(command=self.click_listener_of_button_home)

        ## 今日时间表按键 <- 按键栏  relief=SUNKEN -> 按动无变化
        self.img_courses = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"courses.png"}'))
        self.img_courses_hover = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"courses_hover.png"}'))
        self.img_courses_selected = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"courses_selected.png"}'))
        self.button_courses = Button(master=self.button_panel, image=self.img_courses, bg=values.SIDE_BAR_BG_COLOR, activebackground=values.SIDE_BAR_BG_COLOR, border=0)
        self.button_courses.pack(fill=X, expand=False, side=TOP)
        self.button_courses.bind('<Enter>', lambda e: self.button_courses.configure(image=self.img_courses_hover if (self.current_page!="courses") else self.img_courses_selected))
        self.button_courses.bind('<Leave>', lambda e: self.button_courses.configure(image=self.img_courses if (self.current_page!="courses") else self.img_courses_selected))
        self.button_courses.configure(command=self.click_listener_of_button_courses)

        ## 本周时间表按键 <- 按键栏
        self.img_timetable = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"timetable.png"}'))
        self.img_timetable_hover = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"timetable_hover.png"}'))
        self.img_timetable_selected = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"timetable_selected.png"}'))
        self.button_timetable = Button(master=self.button_panel, image=self.img_timetable, bg=values.SIDE_BAR_BG_COLOR, activebackground=values.SIDE_BAR_BG_COLOR, border=0)
        self.button_timetable.pack(fill=X, expand=False, side=TOP, pady=5)
        self.button_timetable.bind('<Enter>', lambda e: self.button_timetable.configure(image=self.img_timetable_hover if (self.current_page!="timetable") else self.img_timetable_selected))
        self.button_timetable.bind('<Leave>', lambda e: self.button_timetable.configure(image=self.img_timetable if (self.current_page!="timetable") else self.img_timetable_selected))
        self.button_timetable.configure(command=self.click_listener_of_button_timetable)

        ## 登录记录按键 <- 按键栏
        self.img_records = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"records.png"}'))
        self.img_records_hover = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"records_hover.png"}'))
        self.img_records_selected = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"records_selected.png"}'))
        self.button_records = Button(master=self.button_panel, image=self.img_records, bg=values.SIDE_BAR_BG_COLOR, activebackground=values.SIDE_BAR_BG_COLOR, border=0)
        self.button_records.pack(fill=X, expand=False, side=TOP)
        self.button_records.bind('<Enter>', lambda e: self.button_records.configure(image=self.img_records_hover if (self.current_page!="records") else self.img_records_selected))
        self.button_records.bind('<Leave>', lambda e: self.button_records.configure(image=self.img_records if (self.current_page!="records") else self.img_records_selected))
        self.button_records.configure(command=self.click_listener_of_button_records)

        ## 设置按键 <- 按键栏
        self.img_setting = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"setting.png"}'))
        self.img_setting_hover = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"setting_hover.png"}'))
        self.img_setting_selected = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"setting_selected.png"}'))
        self.button_setting = Button(master=self.button_panel, image=self.img_setting, bg=values.SIDE_BAR_BG_COLOR, activebackground=values.SIDE_BAR_BG_COLOR, border=0)
        self.button_setting.pack(fill=X, expand=False, side=TOP, pady=5)
        self.button_setting.bind('<Enter>', lambda e: self.button_setting.configure(image=self.img_setting_hover if (self.current_page!="setting") else self.img_setting_selected))
        self.button_setting.bind('<Leave>', lambda e: self.button_setting.configure(image=self.img_setting if (self.current_page!="setting") else self.img_setting_selected))
        self.button_setting.configure(command=self.click_listener_of_button_setting)

        ## 登出按键 <- 按键栏
        self.img_logout = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"logout.png"}'))
        self.img_logout_hover = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"logout_hover.png"}'))
        self.img_logout_selected = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"logout_selected.png"}'))
        self.button_logout = Button(master=self.button_panel, image=self.img_logout, bg=values.SIDE_BAR_BG_COLOR, activebackground=values.SIDE_BAR_BG_COLOR, border=0)
        self.button_logout.pack(fill=X, expand=False, side=BOTTOM, pady=15)
        self.button_logout.bind('<Enter>', lambda e: self.button_logout.configure(image=self.img_logout_hover if (self.current_page!="logout") else self.img_logout_selected))
        self.button_logout.bind('<Leave>', lambda e: self.button_logout.configure(image=self.img_logout if (self.current_page!="logout") else self.img_logout_selected))
        self.button_logout.configure(command=self.click_listener_of_button_logout)

        ## 显示窗口 <- 基于主窗口
        self.display_panel = Frame(master=self.main_frame, bg=values.ROOT_BG_COLOR)
        self.display_panel.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

        ## 使用登录界面覆盖其他界面
        self.login_panel = LoginFrame(master=self.root, caller=self)
        self.login_panel.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

    def click_listener_of_button_home(self, event=0):
        if (self.current_page != "home"):
            self.current_frame.destroy()
            self.current_frame = HomeFrame(master=self.display_panel, caller=self)
        self.current_page = "home"
        self.remove_decoration_on_side_bar_buttons()
        self.button_home.configure(image=self.img_home_selected)

    def click_listener_of_button_courses(self, event=0):
        if (self.current_page != "courses"):
            self.current_frame.destroy()
            self.current_frame = CoursesFrame(master=self.display_panel, caller=self)
        self.current_page = "courses"
        self.remove_decoration_on_side_bar_buttons()
        self.button_courses.configure(image=self.img_courses_selected)

    def click_listener_of_button_timetable(self, event=0):
        if (self.current_page != "timetable"):
            self.current_frame.destroy()
            self.current_frame = TimeTableFrame(master=self.display_panel, caller=self)
        self.current_page = "timetable"
        self.remove_decoration_on_side_bar_buttons()
        self.button_timetable.configure(image=self.img_timetable_selected)

    def click_listener_of_button_records(self, event=0):
        if (self.current_page != "records"):
            self.current_frame.destroy()
            self.current_frame = RecordsFrame(master=self.display_panel, caller=self)
        self.current_page = "records"
        self.remove_decoration_on_side_bar_buttons()
        self.button_records.configure(image=self.img_records_selected)

    def click_listener_of_button_setting(self, event=0):
        if (self.current_page != "setting"):
            self.current_frame.destroy()
            self.current_frame = SettingFrame(master=self.display_panel, caller=self)
        self.current_page = "setting"
        self.remove_decoration_on_side_bar_buttons()
        self.button_setting.configure(image=self.img_setting_selected)

    def click_listener_of_button_logout(self):
        ## 摧毁当前页面
        if (self.current_page != "logout"):
            self.current_frame.destroy()
            self.current_frame = Frame(master=self.display_panel)
        self.current_page = "logout"
        self.remove_decoration_on_side_bar_buttons()
        self.button_logout.configure(image=self.img_logout_selected)
        ## 重新回到登录页面
        self.login_panel = LoginFrame(master=self.root, caller=self)
        self.login_panel.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)
        ## 发布登出时间
        self.post_logout_time()

    def remove_decoration_on_side_bar_buttons(self):
        self.button_home.configure(image=self.img_home)
        self.button_courses.configure(image=self.img_courses)
        self.button_timetable.configure(image=self.img_timetable)
        self.button_records.configure(image=self.img_records)
        self.button_setting.configure(image=self.img_setting)
        self.button_logout.configure(image=self.img_logout)

    def post_logout_time(self):
        self.controller.post_last_logout_time()

    ## 清空frame内所有的widget
    @staticmethod
    def clear_frame(frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    ## 获取pyinstaller加载外部文件时的地址
    @staticmethod
    def get_resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
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

import values
from roundcornerframe import *
from timetablewidget import *
from courseinfowidget import *

class HomeFrame(Frame):
    def __init__(self, master, caller=None, *args, **kw):

        ## 初始化frame
        Frame.__init__(self, master, bg=values.ROOT_BG_COLOR, *args, **kw)
        self.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

        ## 载入调用函数数据以及控制器
        if (caller==None):
            print("Error: HomeFrame miss caller argument")
            return
        self.caller = caller
        self.controller = getattr(caller, "controller")

        ## 预定义字体
        self.student_info_frame_font = tkFont.Font(size=12, family='Arial')

        ## 构建页面
        self.add_widgets()

    def add_widgets(self):
        ## check is there a course within one hour
        self.current_panel = "course_info" if (self.check_existence_of_course_within_one_hour() == True) else "timetable"

        ## 构建学生资料版
        self.init_student_info_panel()

        if (self.current_panel=="course_info"):
            ## 构建课程资料版
            self.init_course_info_panel()
        elif (self.current_panel=="timetable"):
            ## 构建时间表
            self.init_timetable_panel()

    def init_student_info_panel(self):
        ## 初始化显示变量
        self.student_name = StringVar()
        self.student_uid = StringVar()
        self.student_login_time = StringVar()

        self.add_widgets_student_info_panel()

        self.get_student_info()

    def add_widgets_student_info_panel(self):
        ## 资料面板
        self.student_info_base_frame = RoundCornerFrame(master=self, height=100)
        #self.student_info_base_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.15, anchor=NW)
        self.student_info_base_frame.pack(fill=X, expand=False, side=TOP, padx=40, pady=(40, 0))

        self.student_info_frame = Frame(master=self.student_info_base_frame, bg=values.BOX_BG_COLOR, height=100)
        self.student_info_frame.place(relx=0.05, rely=0.5, relwidth=0.9, height=90, anchor=W)

        ## 名字
        self.student_name_prefix_label = Label(master=self.student_info_frame, text="Student Name: ", bg=values.BOX_BG_COLOR, font=self.student_info_frame_font, anchor=W)
        self.student_name_prefix_label.place(relx=0, rely=0.25, anchor=W)

        ## 名字
        self.student_name_label = Label(master=self.student_info_frame, textvariable=self.student_name, bg=values.BOX_BG_COLOR, font=self.student_info_frame_font, anchor=W)
        self.student_name_label.place(relx=0.15, rely=0.25, anchor=W)

        ## UID
        self.student_uid_prefix_label = Label(master=self.student_info_frame, text="Student ID: ", bg=values.BOX_BG_COLOR, font=self.student_info_frame_font, anchor=W)
        self.student_uid_prefix_label.place(relx=0, rely=0.5, anchor=W)

        ## UID
        self.student_uid_label = Label(master=self.student_info_frame, textvariable=self.student_uid, bg=values.BOX_BG_COLOR, font=self.student_info_frame_font, anchor=W)
        self.student_uid_label.place(relx=0.15, rely=0.5, anchor=W)

        ## 最后登录时间
        self.student_login_time_prefix_label = Label(master=self.student_info_frame, text="Login time: ", bg=values.BOX_BG_COLOR, font=self.student_info_frame_font, anchor=W)
        self.student_login_time_prefix_label.place(relx=0, rely=0.75, anchor=W)

        ## 最后登录时间
        self.student_login_time_label = Label(master=self.student_info_frame, textvariable=self.student_login_time, bg=values.BOX_BG_COLOR, font=self.student_info_frame_font, anchor=W)
        self.student_login_time_label.place(relx=0.15, rely=0.75, anchor=W)

        ## 遮挡右边
        proportion = 0.3
        bias = 1 - proportion
        self.shadow_frame = Frame(master=self.student_info_base_frame, bg=values.ROOT_BG_COLOR)
        self.shadow_frame.place(relx=1, rely=0.5, relwidth=proportion, relheight=1.1, anchor=E)
        self.img_round_corner_NE = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"round_corner_NE.png"}'))
        self.round_corner_NE_label = Label(master=self.student_info_base_frame, image=self.img_round_corner_NE, borderwidth=0)
        self.round_corner_NE_label.place(relx=bias, rely=0, anchor=NE)
        self.img_round_corner_SE = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"round_corner_SE.png"}'))
        self.round_corner_SE_label = Label(master=self.student_info_base_frame, image=self.img_round_corner_SE, borderwidth=0)
        self.round_corner_SE_label.place(relx=bias, rely=1, anchor=SE)

        self.img_potato_normal = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"potato_normal.png"}'))
        self.img_potato_reversed = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"potato_reversed.png"}'))

        self.switch_mode_label = Label(master=self.shadow_frame, image=self.img_potato_normal, bg=values.ROOT_BG_COLOR)
        self.switch_mode_label.place(relx=1, rely=0.5, anchor=E)
        self.switch_mode_label.configure(image=self.img_potato_normal if (self.current_panel == "timetable") else self.img_potato_reversed)

        def switch_function(event):
            if (self.current_panel == "course_info"):
                self.current_panel = "timetable"
                self.switch_mode_label.configure(image=self.img_potato_normal)
                self.course_info_base_frame.destroy()
                self.init_timetable_panel()
            else:
                self.current_panel = "course_info"
                self.switch_mode_label.configure(image=self.img_potato_reversed)
                self.timetable_base_frame.destroy()
                self.init_course_info_panel()

        self.switch_mode_label.bind("<Button-1>", switch_function)

    def init_course_info_panel(self):
        self.add_widgets_course_info_panel()

    def add_widgets_course_info_panel(self):
        self.course_info_base_frame = CourseInfoWidget(master=self, caller=self.caller, course_code=None)

    def init_timetable_panel(self):
        self.add_widgets_timetable_panel()

    def add_widgets_timetable_panel(self):
        self.timetable_base_frame = TimeTableWidget(master=self, caller=self.caller, time_period=(8, 19))

    def check_existence_of_course_within_one_hour(self):
        return self.controller.check_existence_of_course_within_one_hour()

    def get_student_info(self):
        ## 给显示变量赋值
        self.student_name.set(self.controller.get_student_name())
        self.student_uid.set(self.controller.get_student_id())
        self.student_login_time.set(self.controller.get_student_last_login_time())

    ## 获取pyinstaller加载外部文件时的地址
    @staticmethod
    def get_resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    @staticmethod
    def resize(w, h, w_box, h_box, pil_image):
        f1 = w_box / w
        f2 = h_box / h
        factor = max(f1, f2)
        width = int(w * factor)
        height = int(h * factor)
        width = width if width != 0 else 1
        height = height if height != 0 else 1
        return pil_image.resize((width, height), Image.Resampling.LANCZOS)
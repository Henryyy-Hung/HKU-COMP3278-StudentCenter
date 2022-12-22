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
from courseinfowidget import *


class CoursesFrame(Frame):
    def __init__(self, master, caller=None, *args, **kw):

        ## 初始化frame
        Frame.__init__(self, master, bg=values.ROOT_BG_COLOR, *args, **kw)
        self.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

        ## 载入调用函数数据以及控制器
        if (caller==None):
            print("Error: ScheduleFrame miss caller argument")
            return
        self.caller = caller
        self.controller = getattr(caller, "controller")

        ## 初始化课程列表
        self.basic_info_of_all_courses = dict()

        ## 给课程列表赋值
        self.get_basic_info_of_all_courses()

        ## 构建页面
        self.add_widgets()

    def add_widgets(self):
        self.course_selection_pannel = Frame(master=self, bg=values.ROOT_BG_COLOR)
        self.course_selection_pannel.pack(fill=BOTH, expand=True, side=TOP, pady=40, padx=40)

        for idx in range(len(self.basic_info_of_all_courses.keys())):

            course_code = list(self.basic_info_of_all_courses.keys())[idx]
            course_name = self.basic_info_of_all_courses[course_code]["course_name"]
            course_id = self.basic_info_of_all_courses[course_code]["course_id"]
            subclass = self.basic_info_of_all_courses[course_code]["subclass"]
            venue = self.basic_info_of_all_courses[course_code]["venue"]

            item_per_row = 2

            course_panel_base_frame = RoundCornerFrame(master=self.course_selection_pannel, height=100, width=100)
            course_panel_base_frame.grid(column=idx % item_per_row, row=idx // item_per_row, sticky=N + S + W + E, padx=(0 if idx % item_per_row==0 else 15, 15 if idx % item_per_row != item_per_row -1 else 0), pady=(0 if idx // item_per_row==0 else 15, 15))

            self.course_selection_pannel.columnconfigure(idx % item_per_row, weight=1)

            course_panel_frame = Frame(master=course_panel_base_frame, bg=values.BOX_BG_COLOR)
            course_panel_frame.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=1, anchor=W)

            course_code_label = Label(master=course_panel_frame,
                                      text=f"{course_code} {subclass}",
                                      fg='black',
                                      bg=values.BOX_BG_COLOR,
                                      font=tkFont.Font(size=15, family='Arial'),
                                      anchor=W
                                      )
            course_code_label.place(relx=0, rely=0.5, anchor=SW)

            course_name_label = Label(master=course_panel_frame,
                                      text=f"{course_name}",
                                      fg=values.PALE_GRAY,
                                      bg=values.BOX_BG_COLOR,
                                      font=tkFont.Font(size=10, family='Arial'),
                                      anchor=W
                                      )
            course_name_label.place(relx=0, rely=0.5, anchor=NW)

            def click(course_id):
                self.course_info_base_frame = Frame(master=self, bg=values.ROOT_BG_COLOR)
                self.course_info_base_frame.place(relx=0,rely=0,relheight=1,relwidth=1,anchor=NW)

                self.course_info = CourseInfoWidget(master=self.course_info_base_frame, caller=self.caller, course_id=course_id)

                self.bottom_frame = Frame(master=self.course_info_base_frame, bg=values.ROOT_BG_COLOR, height=40)
                self.button_quit = Button(master=self.bottom_frame, text="Back", bg='#282B3D', activebackground='#282B3D', fg='white', activeforeground='white',borderwidth=1, relief=GROOVE,  font=tkFont.Font(size=20, family='Arial'))

                def quit(event=0):
                    self.course_info.destroy()
                    self.bottom_frame.destroy()
                    self.course_info_base_frame.destroy()

                self.course_info.bind('<Escape>', quit)
                self.course_info.bind('<space>', quit)

                self.course_info.focus_set()
                self.button_quit.configure(command=quit)
                self.bottom_frame.pack(fill=X, expand=False, side=TOP, pady=(0,40), padx=40)
                self.button_quit.place(relx=0.5, rely=0.5, relwidth=0.25, relheight=1, anchor=CENTER)

            course_panel_base_frame.bind("<Button-1>", lambda e, course_id=course_id: click(course_id))
            course_panel_frame.bind("<Button-1>", lambda e, course_id=course_id: click(course_id))
            course_code_label.bind("<Button-1>", lambda e, course_id=course_id: click(course_id))
            course_name_label.bind("<Button-1>", lambda e, course_id=course_id: click(course_id))


    def get_basic_info_of_all_courses(self):
        course_id_of_all_courses = self.controller.get_all_courses_course_id()
        for course_id in course_id_of_all_courses:
            course_code = self.controller.get_course_code_by_course_id(course_id)
            course_name = self.controller.get_course_name_by_course_id(course_id)
            subclass = self.controller.get_subclass_by_course_id(course_id)
            venue = self.controller.get_venue_by_course_id(course_id)
            info = {"course_id":course_id,
                    "course_name":course_name,
                    "subclass":subclass,
                    "venue":venue}
            self.basic_info_of_all_courses[course_code] = info








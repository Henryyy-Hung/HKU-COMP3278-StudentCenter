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
from dateentrywidget import *

class TimeTableWidget(RoundCornerFrame):
    def __init__(self, master, caller=None, time_period=(8, 20), date=None, *args, **kw):
        ## 初始化一个圆角frame
        RoundCornerFrame.__init__(self, master, *args, **kw)
        self.pack(fill=BOTH, expand=True, side=TOP, padx=40, pady=(40,40))

        ## 载入调用函数数据以及控制器
        if (caller == None):
            print("Error: TimeTableWidget miss caller argument")
            return
        self.caller = caller
        self.controller = getattr(caller, "controller")

        ## 定义变量
        self.date = date
        self.days_of_the_week = list()
        self.time_slots = list()
        self.timetable_cols = 7
        self.timetable_rows = (time_period[1] - time_period[0])
        self.timetable_start_time = time_period[0]

        ## 获取所有在date所属星期内的日子的datetime对象
        self.get_days_of_the_week()
        ## 根据这些日子，从数据库获取数据
        self.get_timetable_info()

        ## 构建页面
        self.add_widgets()

    def add_widgets(self):
        self.base_frame = Frame(master=self, bg=values.BOX_BG_COLOR)
        self.base_frame.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.9, anchor=W)

        self.title_label = Label(master=self.base_frame, text="WEEKLY TIME TABLE", fg=values.PALE_GRAY, bg=values.BOX_BG_COLOR, font=tkFont.Font(size=25, family='Arial'), anchor=W)
        self.title_label.pack(fill=X, side=TOP, pady=(0, 20))

        self.content_frame = Frame(master=self.base_frame, bg=values.BOX_BG_COLOR)
        self.content_frame.pack(fill=BOTH, expand=True, side=TOP, pady=(0, 10))

        self.left_margin = 1 / 10
        self.right_margin = 0

        self.left_table_frame = Frame(master=self.content_frame, bg=values.BOX_BG_COLOR)
        self.left_table_frame.place(relx=0, rely=0, relwidth=self.left_margin, relheight=1, anchor=NW)

        self.center_table_frame = Frame(master=self.content_frame, bg=values.BOX_BG_COLOR)
        self.center_table_frame.place(relx=self.left_margin, rely=0, relwidth=1 - self.left_margin - self.right_margin, relheight=1, anchor=NW)

        self.right_table_frame = Frame(master=self.content_frame, bg=values.BOX_BG_COLOR)
        self.right_table_frame.place(relx=1, rely=0, relwidth=self.right_margin, relheight=1, anchor=NE)

        self.center_table_heading_frame = Frame(master=self.center_table_frame, bg=values.BOX_BG_COLOR)
        self.center_table_heading_frame.place(relx=0, rely=0, relwidth=1, relheight=1 / (self.timetable_rows + 1), anchor=NW)

        self.center_table_content_frame = Frame(master=self.center_table_frame, bg=values.BOX_BG_COLOR)
        self.center_table_content_frame.place(relx=0, rely=1 / (self.timetable_rows + 1), relwidth=1, relheight=1 - 1 / (self.timetable_rows + 1), anchor=NW)

        ## 初始化y轴时间坐标
        for row in range(1, self.timetable_rows):
            displayed_time = self.timetable_start_time + row
            text = f'{displayed_time}:00  -  '
            indicator_label = Label(master=self.left_table_frame,
                                    text=text,
                                    bg=values.BOX_BG_COLOR,
                                    borderwidth=0,
                                    anchor=E)
            indicator_label.place(relx=0, rely=(1 / (self.timetable_rows + 1)) * (row + 0.5), relwidth=1, relheight=(1 / (self.timetable_rows + 1)), anchor=NW)

        ## 初始化x轴日期坐标
        for col in range(self.timetable_cols):
            text = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][col]
            bg = values.BOX_BG_COLOR # if col != self.date.weekday() else values.TIMETABLE_HIGHLIGHT_COLOR
            heading_label = Label(master=self.center_table_heading_frame,
                                  text=f"{text}",
                                  bg=bg,
                                  borderwidth=0)
            heading_label.place(relx=(1 / self.timetable_cols) * col, rely=0, relwidth=(1 / self.timetable_cols), relheight=1, anchor=NW)

        ## 绘制格子
        for col in range(self.timetable_cols+1):
            if (col == self.date.weekday() and True):
                highlight_background = Label(master=self.center_table_content_frame, bg=values.TIMETABLE_HIGHLIGHT_COLOR, borderwidth=0)
                highlight_background.place(relx=(1/self.timetable_cols)*col, rely=0, relwidth=(1/self.timetable_cols), relheight=1, anchor=NW)

            vertical_line = Label(master=self.center_table_content_frame,
                                  bg=values.ROOT_BG_COLOR,
                                  borderwidth=0)
            if (col != self.timetable_cols):
                vertical_line.place(relx=(1/self.timetable_cols)*col, rely=0, width=1, relheight=1, anchor=NW)
            else:
                vertical_line.place(relx=(1/self.timetable_cols)*col, rely=0, width=1, relheight=1, anchor=NE)

        for row in range(self.timetable_rows+1):
            horizontal_line = Label(master=self.center_table_content_frame,
                                    bg=values.ROOT_BG_COLOR,
                                    borderwidth=0)

            if (row != self.timetable_rows):
                horizontal_line.place(relx=0, rely=(1/self.timetable_rows)*row, relwidth=1, height=1, anchor=NW)
            else:
                horizontal_line.place(relx=0, rely=(1/self.timetable_rows)*row, relwidth=1, height=1, anchor=SW)

        ## 绘制格子
        for col in range(8):
            vertical_line = Label(master=self.center_table_heading_frame,
                                  bg=values.ROOT_BG_COLOR,
                                  borderwidth=0)
            if (col != self.timetable_cols):
                vertical_line.place(relx=(1/self.timetable_cols)*col, rely=0, width=1, relheight=1, anchor=NW)
            else:
                vertical_line.place(relx=(1/self.timetable_cols)*col, rely=0, width=1, relheight=1, anchor=NE)

        for row in range(1):
            horizontal_line = Label(master=self.center_table_heading_frame,
                                    bg=values.ROOT_BG_COLOR,
                                    borderwidth=0)
            horizontal_line.place(relx=0, rely=(1 / self.timetable_rows) * row, relwidth=1, height=1, anchor=NW)

        ## 为课程分配颜色
        idx = 0
        self.color_map = dict()
        for time_slot in self.time_slots:
            course_code = time_slot[0]
            if course_code not in self.color_map.keys():
                self.color_map[course_code] = values.TIMETABLE_BG_COLORS[idx]
                idx += 1
                if (idx >= len(values.TIMETABLE_BG_COLORS)):
                    idx = 0

        ## 将课程块放进时间表
        for time_slot in self.time_slots:
            text, col, row, duration = time_slot[0], time_slot[1], time_slot[2] - self.timetable_start_time, time_slot[3] - time_slot[2]
            temp = Label(master=self.center_table_content_frame,
                         text=text,
                         fg='white',
                         bg=self.color_map[text],
                         borderwidth=0,
                         anchor=N)
            temp.place(relx=col * (1 / self.timetable_cols),
                       rely=row * (1 / self.timetable_rows),
                       relwidth=(1 / self.timetable_cols),
                       relheight=(1 / self.timetable_rows) * duration,
                       anchor=NE)

        current_time = datetime.datetime.now()
        arrow_position = current_time.hour + current_time.minute / 60
        if (not arrow_position < self.timetable_start_time and not arrow_position > (self.timetable_start_time+self.timetable_rows)):
            self.current_time_line_label = Label(master=self.center_table_content_frame, bg='#3F40DF', borderwidth=0, anchor=W)
            self.current_time_line_label.place(relx=0, rely=(1/(self.timetable_rows)*(arrow_position-self.timetable_start_time)), relwidth=1, height=1, anchor=W)

        self.time_pointer()

    def time_pointer(self):
        ## 初始化时间指针
        current_time  = datetime.datetime.now()
        arrow_position = current_time.hour + current_time.minute / 60
        if (not arrow_position < self.timetable_start_time and not arrow_position > (self.timetable_start_time+self.timetable_rows)):
            self.current_time_line_label.place(relx=0, rely=(1/(self.timetable_rows)*(arrow_position-self.timetable_start_time)), relwidth=1, height=1, anchor=W)
        self.after(1000, self.time_pointer)

    def get_days_of_the_week(self):
        self.days_of_the_week.clear()
        if (not isinstance(self.date, datetime.datetime)):
            self.date = datetime.datetime.now()
        state = 0
        for idx in range(-6, 7):
            temp_date = self.date + datetime.timedelta(days=idx)
            if (temp_date.weekday() == 0):
                state = 1
            if (state==1):
                self.days_of_the_week.append(temp_date)
            if (state==1 and temp_date.weekday() == 6):
                break

    def get_timetable_info(self):
        self.time_slots = self.controller.get_time_slots_of_the_week(self.days_of_the_week.copy())

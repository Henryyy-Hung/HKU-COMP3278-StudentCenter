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
from timetablewidget import *

class TimeTableFrame(Frame):
    def __init__(self, master, caller=None, *args, **kw):

        ## 初始化frame
        Frame.__init__(self, master, bg=values.ROOT_BG_COLOR, *args, **kw)
        self.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

        ## 载入调用函数数据以及控制器
        if (caller==None):
            print("Error: TimeTableFrame miss caller argument")
            return
        self.caller = caller
        self.controller = getattr(caller, "controller")

        ## 构建页面
        self.add_widgets()

    def add_widgets(self):
        self.timetable_base_frame = TimeTableWidget(master=self, caller=self.caller, time_period=(0, 24))
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

class RoundCornerFrame(Frame):
    def __init__(self, master, *args, **kw):

        ## 初始化frame
        Frame.__init__(self, master, bg=values.BOX_BG_COLOR, *args, **kw)

        ## 构建页面
        self.add_corner_widgets()

    def add_corner_widgets(self):
        ## 圆角图标
        self.img_round_corner_NE = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"round_corner_NE.png"}'))
        self.img_round_corner_NW = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"round_corner_NW.png"}'))
        self.img_round_corner_SE = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"round_corner_SE.png"}'))
        self.img_round_corner_SW = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"round_corner_SW.png"}'))

        ## 放置圆角
        self.round_corner_NE_label = Label(self, image=self.img_round_corner_NE, borderwidth=0).place(relx=1, rely=0, anchor=NE)
        self.round_corner_NW_label = Label(self, image=self.img_round_corner_NW, borderwidth=0).place(relx=0, rely=0, anchor=NW)
        self.round_corner_SE_label = Label(self, image=self.img_round_corner_SE, borderwidth=0).place(relx=1, rely=1, anchor=SE)
        self.round_corner_SW_label = Label(self, image=self.img_round_corner_SW, borderwidth=0).place(relx=0, rely=1, anchor=SW)

    ## 获取pyinstaller加载外部文件时的地址
    @staticmethod
    def get_resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
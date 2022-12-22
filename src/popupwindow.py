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

class WelcomeTopBar(Toplevel):
    def __init__(self, master, *args, **kw):
        self.image = PhotoImage(file=self.get_resource_path(f'./{"res"}{os.sep}{"drawable"}{os.sep}{"top_bar_welcome.png"}'))

        self.width = self.image.width()
        self.height = self.image.height()

        Toplevel.__init__(self, master, *args, **kw)

        self.attributes("-transparentcolor", "#F0F0F0")
        self.overrideredirect(True)
        self.resizable(False, False)
        self.attributes("-alpha", 0)

        self.bind("<Button-1>", lambda e: self.destroy())

        alignstr = f'{self.width}x{self.height}+{int(master.winfo_x() + (master.winfo_width() - 240 - self.width) / 2) + 240}+{int(master.winfo_y() + 45)}'
        self.geometry(alignstr)

        self.label = Label(self, image=self.image, bd=0)
        self.label.place(x=0, y=0, width=self.width, height=self.height)
        self.label.pack()

        self.fps = 30
        self.duration = 2.5

        self.fade_in_duration = 0.5
        self.fade_away_duration = 0.5
        self.fade_away_start_time = 1.2
        self.fade_in()
        self.fade_away()

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 0.9:
            alpha += 1/(self.fade_in_duration * self.fps)
            self.attributes("-alpha", alpha)
            self.after(int(1000/self.fps), self.fade_in)

    def fade_away(self):
        alpha = self.attributes("-alpha")
        if self.fade_away_start_time <= 0:
            if alpha > 0:
                alpha -= 1/(self.fade_away_duration*self.fps)
                self.attributes("-alpha", alpha)
                self.after(int(1000/self.fps), self.fade_away)
            else:
                self.destroy()
        else:
            self.fade_away_start_time -= 0.1
            self.after(100, self.fade_away)

    ## 获取pyinstaller加载外部文件时的地址
    @staticmethod
    def get_resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

class EmailSentTopBar(Toplevel):
    def __init__(self, master, *args, **kw):
        self.image = PhotoImage(file=self.get_resource_path(f'./{"res"}{os.sep}{"drawable"}{os.sep}{"top_bar_email_sent.png"}'))

        self.width = self.image.width()
        self.height = self.image.height()

        Toplevel.__init__(self, master, *args, **kw)

        self.attributes("-transparentcolor", "#F0F0F0")
        self.overrideredirect(True)
        self.resizable(False, False)
        self.attributes("-alpha", 0)

        self.bind("<Button-1>", lambda e: self.destroy())

        alignstr = f'{self.width}x{self.height}+{int(master.winfo_x() + (master.winfo_width() - 240 - self.width) / 2) + 240}+{int(master.winfo_y() + 45)}'
        self.geometry(alignstr)

        self.label = Label(self, image=self.image, bd=0)
        self.label.place(x=0, y=0, width=self.width, height=self.height)
        self.label.pack()

        self.fps = 30
        self.duration = 2.5

        self.fade_in_duration = 0.5
        self.fade_away_duration = 0.5
        self.fade_away_start_time = 1
        self.fade_in()
        self.fade_away()

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 0.9:
            alpha += 1/(self.fade_in_duration * self.fps)
            self.attributes("-alpha", alpha)
            self.after(int(1000/self.fps), self.fade_in)

    def fade_away(self):
        alpha = self.attributes("-alpha")
        if self.fade_away_start_time <= 0:
            if alpha > 0:
                alpha -= 1/(self.fade_away_duration*self.fps)
                self.attributes("-alpha", alpha)
                self.after(int(1000/self.fps), self.fade_away)
            else:
                self.destroy()
        else:
            self.fade_away_start_time -= 0.1
            self.after(100, self.fade_away)

    ## 获取pyinstaller加载外部文件时的地址
    @staticmethod
    def get_resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
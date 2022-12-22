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


class SettingFrame(Frame):
    def __init__(self, master, caller=None, *args, **kw):

        ## 初始化frame
        Frame.__init__(self, master, bg=values.ROOT_BG_COLOR, *args, **kw)
        self.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

        ## 载入调用函数数据以及控制器
        if (caller==None):
            print("Error: SettingFrame miss caller argument")
            return
        self.caller = caller
        self.controller = getattr(caller, "controller")

        ## 变量用以储存学生email
        self.student_email = StringVar()
        self.get_student_email()

        ## 构建页面
        self.add_widgets()

    def add_widgets(self):
        self.email_setting_base_frame = RoundCornerFrame(master=self, height=100)
        #self.student_info_base_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.15, anchor=NW)
        self.email_setting_base_frame.pack(fill=X, expand=False, side=TOP, padx=40, pady=40)

        self.email_setting_frame = Frame(master=self.email_setting_base_frame, bg=values.BOX_BG_COLOR, height=100)
        self.email_setting_frame.place(relx=0.05, rely=0.5, relwidth=0.9, height=90, anchor=W)

        self.setting_frame_font_title = tkFont.Font(size=15, family='Arial')
        self.setting_frame_font_calibre = tkFont.Font(size=10, family='Arial')

        self.email_setting_title_label = Label(master=self.email_setting_frame, text=f"Email", bg=values.BOX_BG_COLOR, font=self.setting_frame_font_title)
        self.email_setting_title_label.place(relx=0, rely=0.3, anchor=W)

        self.student_email_label = Label(master=self.email_setting_frame, textvariable=self.student_email, bg=values.BOX_BG_COLOR, font=self.setting_frame_font_calibre)
        self.student_email_label.place(relx=0, rely=0.7, anchor=W)

        self.change_student_name_label = Label(master=self.email_setting_frame, text="Change", bg=values.BOX_BG_COLOR, fg=values.SETTING_TEXT_NORMAL_FG_COLOR, font=self.setting_frame_font_calibre)
        self.change_student_name_label.place(relx=1, rely=0.7, anchor=E)
        self.change_student_name_label.bind('<Enter>', lambda e: self.change_student_name_label.configure(fg=values.SETTING_TEXT_HOVER_FG_COLOR))
        self.change_student_name_label.bind('<Leave>', lambda e: self.change_student_name_label.configure(fg=values.SETTING_TEXT_NORMAL_FG_COLOR))
        self.change_student_name_label.bind('<Button-1>', self.change_email)

    def change_email(self, event=0):
        pop_up_window = Toplevel(master=self, bg=values.BOX_BG_COLOR)
        pop_up_window_width = 500
        pop_up_window_height = 200
        alignstr = f'{int(pop_up_window_width)}x{int(pop_up_window_height)}+{int((self.winfo_screenwidth() - pop_up_window_width) / 2)}+{int((self.winfo_screenheight() - pop_up_window_height) / 2)}'
        pop_up_window.geometry(alignstr)
        pop_up_window.overrideredirect(True)
        pop_up_window.grab_set()  # 置顶页面

        base_frame = Frame(master=pop_up_window, bg=values.BOX_BG_COLOR, highlightbackground=values.SIDE_BAR_BG_COLOR, highlightthickness=1)
        base_frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

        top_frame =  Frame(master=base_frame, bg=values.SIDE_BAR_BG_COLOR)
        top_frame.place(relx = 0.5, rely=0, relwidth=1, relheight=0.3, anchor=N)

        bottom_frame =  Frame(master=base_frame, bg=values.BOX_BG_COLOR)
        bottom_frame.place(relx = 0.5, rely=0.3, relwidth=1, relheight=0.7, anchor=N)

        title_label =  Label(master=top_frame, text=f"Change Email", bg=values.SIDE_BAR_BG_COLOR, fg = 'white', font=tkFont.Font(size=20, family='Arial'))
        title_label.place(relx=0.1, rely=0.5, anchor=W)

        title_label_2 = Label(master=bottom_frame, text=f"New Email", bg=values.BOX_BG_COLOR, fg = 'black', font=tkFont.Font(size=12, family='Arial'), anchor=W)
        title_label_2.pack(fill=X, expand=False, side=TOP, padx=50, pady=10)

        new_email_entry = Entry(master=bottom_frame, borderwidth=1, bg=values.ROOT_BG_COLOR)
        new_email_entry.pack(fill=X, expand=False, side=TOP, padx=50, pady=(0, 10))
        new_email_entry.focus_set()

        def confirm_change():
            self.post_new_student_email(new_email_entry.get())
            pop_up_window.destroy()

        save_button = Button(master=bottom_frame, text="  Save  ", bg='#282B3D', activebackground='#282B3D', fg='white', activeforeground='white',borderwidth=1, command=lambda : confirm_change(), relief=GROOVE)
        save_button.pack(fill=X, expand=False, side=RIGHT, padx=(5, 50), pady=(0, 10))

        cancel_button = Button(master=bottom_frame, text=" Cancel ", bg='#FFFFFF', activebackground='#FFFFFF', fg='black', activeforeground='black',borderwidth=1, command=lambda :pop_up_window.destroy(), relief=GROOVE)
        cancel_button.pack(fill=X, expand=False, side=RIGHT, padx=(50, 5), pady=(0, 10))

        new_email_entry.bind("<KeyRelease-Return>", lambda e: save_button.invoke())
        pop_up_window.bind('<Escape>', lambda e: cancel_button.invoke())


    def get_student_email(self):
        self.student_email.set(self.controller.get_student_email())

    def post_new_student_email(self, new_student_email_address):
        self.controller.post_new_student_email(new_student_email_address)
        self.get_student_email()




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


class RecordsFrame(Frame):
    def __init__(self, master, caller=None, *args, **kw):
        ## 初始化frame
        Frame.__init__(self, master, bg=values.ROOT_BG_COLOR, *args, **kw)
        self.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

        ## 载入调用函数数据以及控制器
        if (caller==None):
            print("Error: RecordsFrame miss caller argument")
            return
        self.caller = caller
        self.controller = getattr(caller, "controller")

        ## 构建页面
        self.add_widgets()

        self.init_records_panel()

    def add_widgets(self):
        pass

    def init_records_panel(self):
        self.records = []
        self.get_records()
        self.add_widgets_records_panel()

    def add_widgets_records_panel(self):
        self.records_base_frame = RoundCornerFrame(master=self)
        self.records_base_frame.pack(fill=BOTH, expand=True, side=TOP, padx=40, pady=40)

        self.records_frame = Frame(master=self.records_base_frame, bg=values.BOX_BG_COLOR)
        self.records_frame.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.9, anchor=W)

        self.title_label = Label(master=self.records_frame, text="User Login History", fg=values.PALE_GRAY, bg=values.BOX_BG_COLOR, font=tkFont.Font(size=25, family='Arial'), anchor=W)
        self.title_label.pack(fill=X, side=TOP, pady=(0, 20))

        # Create an instance of ttk
        style = ttk.Style()
        style.map('Treeview', background=[('selected', 'white')])
        style.map('Treeview', foreground=[('selected', 'black')])
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        style.configure("Treeview.Heading", font=("Arial", 13))
        style.configure("Treeview", rowheight=30, font=("Arial", 11))

        self.scrollbar_records_frame = ttk.Scrollbar(self.records_frame)
        self.scrollbar_records_frame.pack(side="right", fill="y")

        self.records_tree = ttk.Treeview(
            master=self.records_frame,
            columns=("Login Time", "Logout Time", "Duration"),
            selectmode="browse",
            show=("tree", "headings"),
            yscrollcommand=self.scrollbar_records_frame.set,
            style="mystyle.Treeview"
        )
        self.scrollbar_records_frame.config(command=self.records_tree.yview)

        self.records_tree.column("#0", anchor="w", width=100)
        self.records_tree.column("Login Time", anchor="w", width=100)
        self.records_tree.column("Logout Time", anchor="w", width=100)
        self.records_tree.column("Duration", anchor="w", width=100)

        self.records_tree.heading("#0", text="Index", anchor="w" )
        self.records_tree.heading("Login Time", text="Login Time", anchor="w", )
        self.records_tree.heading("Logout Time", text="Logout Time", anchor="w", )
        self.records_tree.heading("Duration", text="Duration", anchor="w", )

        self.records_tree.pack(expand=True, fill="both", padx=(40,0))

        for idx in range(len(self.records)):
            login, logout, duration = self.records[idx]
            self.records_tree.insert(parent="", index="end", iid=idx, text=f"{idx}", values=(login, logout, duration))

    def get_records(self):
        self.records = self.controller.get_login_records()


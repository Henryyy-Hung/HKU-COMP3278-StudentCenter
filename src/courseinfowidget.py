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
from popupwindow import *


class CourseInfoWidget(RoundCornerFrame):

    def __init__(self, master, caller=None, course_id=None, *args, **kw):
        ## 初始化一个圆角frame
        RoundCornerFrame.__init__(self, master, *args, **kw)
        self.pack(fill=BOTH, expand=True, side=TOP, padx=40, pady=(40,40))

        ## 载入调用函数数据以及控制器
        if (caller == None):
            print("Error: CourseInfoWidget miss caller argument")
            return
        self.caller = caller
        self.controller = getattr(caller, "controller")
        
        self.course_id = course_id

        self.course_code = StringVar()
        self.course_name = StringVar()
        self.course_subclass = StringVar()
        self.course_venue = StringVar()
        self.course_lecturer = StringVar()

        self.course_message = []
        self.course_material = []
        self.course_zoom_link = []

        self.get_course_info()
        self.get_course_message()
        self.get_course_material()
        self.get_course_zoom_link()

        self.add_widgets_course_info_panel()

    def add_widgets_course_info_panel(self):
        self.base_frame = Frame(master=self, bg=values.BOX_BG_COLOR)
        self.base_frame.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.9, anchor=W)

        self.course_code_label = Label(master=self.base_frame, textvariable=self.course_code,  bg=values.BOX_BG_COLOR, font=tkFont.Font(size=25, family='Arial'), anchor=W)
        self.course_code_label.pack(fill=X, side=TOP)

        self.course_basic_info_frame = Frame(master=self.base_frame, bg=values.BOX_BG_COLOR, height=110)
        self.course_basic_info_frame.pack(fill=X, side=TOP)

        self.course_name_prefix_label = Label(master=self.course_basic_info_frame, text="Name:", bg=values.BOX_BG_COLOR, font=tkFont.Font(size=12, family='Arial'), anchor=W)
        self.course_name_prefix_label.place(relx=0, rely=0.2, anchor=W)

        self.course_name_label = Label(master=self.course_basic_info_frame, textvariable=self.course_name, bg=values.BOX_BG_COLOR, font=tkFont.Font(size=12, family='Arial'), anchor=W)
        self.course_name_label.place(relx=0.15, rely=0.2, anchor=W)

        self.course_subclass_prefix_label = Label(master=self.course_basic_info_frame, text="subclass:", bg=values.BOX_BG_COLOR, font=tkFont.Font(size=12, family='Arial'), anchor=W)
        self.course_subclass_prefix_label.place(relx=0, rely=0.4, anchor=W)

        self.course_subclass_label = Label(master=self.course_basic_info_frame, textvariable=self.course_subclass, bg=values.BOX_BG_COLOR, font=tkFont.Font(size=12, family='Arial'), anchor=W)
        self.course_subclass_label.place(relx=0.15, rely=0.4, anchor=W)

        self.course_venue_prefix_label = Label(master=self.course_basic_info_frame, text="Venue:", bg=values.BOX_BG_COLOR, font=tkFont.Font(size=12, family='Arial'), anchor=W)
        self.course_venue_prefix_label.place(relx=0, rely=0.6, anchor=W)

        self.course_venue_label = Label(master=self.course_basic_info_frame, textvariable=self.course_venue, bg=values.BOX_BG_COLOR, font=tkFont.Font(size=12, family='Arial'), anchor=W)
        self.course_venue_label.place(relx=0.15, rely=0.6, anchor=W)

        self.course_lecturer_prefix_label = Label(master=self.course_basic_info_frame, text="Lecturer:", bg=values.BOX_BG_COLOR, font=tkFont.Font(size=12, family='Arial'), anchor=W)
        self.course_lecturer_prefix_label.place(relx=0, rely=0.8, anchor=W)

        self.course_lecturer_label = Label(master=self.course_basic_info_frame, textvariable=self.course_lecturer, bg=values.BOX_BG_COLOR, font=tkFont.Font(size=12, family='Arial'), anchor=W)
        self.course_lecturer_label.place(relx=0.15, rely=0.8, anchor=W)

        # Create an instance of ttk
        style = ttk.Style()
        # Define Style for Notebook widget
        style.layout("Tab", [('Notebook.tab', {'sticky': 'nswe', 'children':
            [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                [('Notebook.label', {'side': 'top', 'sticky': ''})],
                                   })],
                                               })]
                     )
        # Use the Defined Style to remove the dashed line from Tabs
        style.configure("Tab", focuscolor=style.configure(".")["background"])
        style.configure("Tab", font=("Arial", 12))

        style.configure("TNotebook", background='white')
        style.map('Treeview', background=[('selected', '#EAEEF1')])
        style.map('Treeview', foreground=[('selected', 'black')])
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        style.configure("Treeview.Heading", font=("Arial", 12))
        style.configure("Treeview", rowheight=30, font=("Arial", 11))

        tabControl = ttk.Notebook(self.base_frame)

        self.course_message_panel = Frame(tabControl, bg=values.BOX_BG_COLOR)
        self.scrollbar_course_message_panel = ttk.Scrollbar(self.course_message_panel)
        self.scrollbar_course_message_panel.pack(side="right", fill="y")

        self.course_material_panel = Frame(tabControl, bg=values.BOX_BG_COLOR)
        self.scrollbar_course_material_panel = ttk.Scrollbar(self.course_material_panel)
        self.scrollbar_course_material_panel.pack(side="right", fill="y")

        self.course_zoom_link_panel = Frame(tabControl, bg=values.BOX_BG_COLOR)
        self.scrollbar_course_zoom_link_panel = ttk.Scrollbar(self.course_zoom_link_panel)
        self.scrollbar_course_zoom_link_panel.pack(side="right", fill="y")

        tabControl.add(self.course_message_panel, text=' Message ')
        tabControl.add(self.course_zoom_link_panel, text=' Zoom link ')
        tabControl.add(self.course_material_panel, text=' Course Material ')

        tabControl.pack(fill=BOTH, expand=True, side=TOP, pady=10)

        self.course_message_tree = ttk.Treeview(
            master=self.course_message_panel,
            columns=("Title", "Name", "Message"),
            selectmode="browse",
            show=("tree", "headings"),
            yscrollcommand=self.scrollbar_course_message_panel.set,
            style="mystyle.Treeview"
        )
        self.scrollbar_course_message_panel.config(command=self.course_message_tree.yview)

        self.course_message_tree.column("#0", anchor="w", width=0, stretch=NO)
        self.course_message_tree.column("Title", anchor="w", width=100)
        self.course_message_tree.column("Name", anchor="w", width=100)
        self.course_message_tree.column("Message", anchor="w", width=600)

        self.course_message_tree.heading("#0", text="", anchor="w", )
        self.course_message_tree.heading("Title", text="Title", anchor="w", )
        self.course_message_tree.heading("Name", text="Name", anchor="w", )
        self.course_message_tree.heading("Message", text="Message", anchor="w", )

        self.course_message_tree.pack(expand=True, fill="both")
        self.course_message_tree.bind("<Double-1>", self.link_course_message_tree)

        self.course_zoom_link_tree = ttk.Treeview(
            master=self.course_zoom_link_panel,
            columns=("Name", "Link"),
            selectmode="browse",
            show=("tree", "headings"),
            yscrollcommand=self.scrollbar_course_zoom_link_panel.set,
            style="mystyle.Treeview"
        )
        self.scrollbar_course_zoom_link_panel.config(command=self.course_zoom_link_tree.yview)

        self.course_zoom_link_tree.column("#0", anchor="w", width=0, stretch=NO)
        self.course_zoom_link_tree.column("Name", anchor="w", width=100)
        self.course_zoom_link_tree.column("Link", anchor="w", width=500)

        self.course_zoom_link_tree.heading("#0", text="", anchor="w", )
        self.course_zoom_link_tree.heading("Name", text="Name", anchor="w", )
        self.course_zoom_link_tree.heading("Link", text="Link", anchor="w", )

        self.course_zoom_link_tree.pack(expand=True, fill="both")
        self.course_zoom_link_tree.bind("<Double-1>", self.link_course_zoom_link_tree)

        self.course_material_tree = ttk.Treeview(
            master=self.course_material_panel,
            columns=("Category", "Name", "Link"),
            selectmode="browse",
            show=("tree", "headings"),
            yscrollcommand=self.scrollbar_course_material_panel.set,
            style="mystyle.Treeview"
        )
        self.scrollbar_course_material_panel.config(command=self.course_material_tree.yview)

        self.course_material_tree.column("#0", anchor="w", width=0, stretch=NO)
        self.course_material_tree.column("Category", anchor="w", width=100)
        self.course_material_tree.column("Name", anchor="w", width=260)
        self.course_material_tree.column("Link", anchor="w", width=550)

        self.course_material_tree.heading("#0", text="", anchor="w", )
        self.course_material_tree.heading("Category", text="Category", anchor="w", )
        self.course_material_tree.heading("Name", text="Name", anchor="w", )
        self.course_material_tree.heading("Link", text="Link", anchor="w", )

        self.course_material_tree.pack(expand=True, fill="both")
        self.course_material_tree.bind("<Double-1>", self.link_course_material_tree)


        for idx in range(len(self.course_message)):
            title, name, message = self.course_message[idx]
            self.course_message_tree.insert(parent="", index="end", iid=idx, text="", values=(title, name, message))

        for idx in range(len(self.course_material)):
            category, name, link = self.course_material[idx]
            self.course_material_tree.insert(parent="", index="end", iid=idx, text="", values=(category, name, link))

        for idx in range(len(self.course_zoom_link)):
            name, link = self.course_zoom_link[idx]
            self.course_zoom_link_tree.insert(parent="", index="end", iid=idx, text="", values=(name, link))

        self.img_send_mail = PhotoImage(file=self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"send_mail.png"}'))
        self.img_send_mail_hover = PhotoImage(file=self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"send_mail_hover.png"}'))
        self.img_send_mail_selected = PhotoImage(file=self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"send_mail_selected.png"}'))

        self.email_sent = False
        self.send_mail_label = Label(master=self.base_frame, image=self.img_send_mail, borderwidth=0)
        self.send_mail_label.place(relx=1, rely=0, anchor=NE)
        self.send_mail_label.bind('<Enter>', lambda e: self.send_mail_label.configure(image=self.img_send_mail_hover))
        self.send_mail_label.bind('<Leave>', lambda e: self.send_mail_label.configure(image=self.img_send_mail))
        self.send_mail_label.bind("<Button-1>", self.send_mail)

    def link_course_message_tree(self, event):
        input_id = self.course_message_tree.selection()
        col = int(self.course_message_tree.identify_column(event.x)[1:])-1
        col = 0 if col < 0 else col
        input_item = self.course_message_tree.item(input_id, "values")
        if (len(input_item)<=col):
            return False

    def link_course_zoom_link_tree(self, event):
        input_id = self.course_zoom_link_tree.selection()
        col = int(self.course_zoom_link_tree.identify_column(event.x)[1:])-1
        col = 0 if col < 0 else col
        input_item = self.course_zoom_link_tree.item(input_id, "values")
        if (len(input_item)<=col):
            return False
        if (col == 1):
            webbrowser.open(input_item[col])

    def link_course_material_tree(self, event):
        input_id = self.course_material_tree.selection()
        col = int(self.course_material_tree.identify_column(event.x)[1:])-1
        col = 0 if col < 0 else col
        input_item = self.course_material_tree.item(input_id, "values")
        if (len(input_item)<=col):
            return False
        if (col == 2):
            webbrowser.open(input_item[col])

    def send_mail(self, event=0):
        ## update self label
        self.send_mail_label.configure(image=self.img_send_mail_selected)
        self.send_mail_label.bind('<Enter>', lambda e: self.send_mail_label.configure(image=self.img_send_mail_selected))
        self.send_mail_label.bind('<Leave>', lambda e: self.send_mail_label.configure(image=self.img_send_mail_selected))
        if (self.email_sent==False):
            self.controller.send_email_regarding_course_info_by_course_id(self.course_id)
            notice = EmailSentTopBar(master=self.caller.root)
        self.email_sent = True

    def get_course_info(self):
        if (not isinstance(self.course_id, str)):
            self.course_id = self.controller.get_next_course_course_id()
        self.course_code.set(self.controller.get_course_code_by_course_id(self.course_id))
        self.course_name.set(self.controller.get_course_name_by_course_id(self.course_id))
        self.course_subclass.set(self.controller.get_subclass_by_course_id(self.course_id))
        self.course_venue.set(self.controller.get_venue_by_course_id(self.course_id))
        self.course_lecturer.set(self.controller.get_lecturer_by_course_id(self.course_id))

    def get_course_message(self):
        self.course_message = self.controller.get_messages_by_course_id(self.course_id)

    def get_course_zoom_link(self):
        self.course_zoom_link = self.controller.get_zoom_links_by_course_id(self.course_id)

    def get_course_material(self):
        self.course_material = self.controller.get_materials_by_course_id(self.course_id)

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
from popupwindow import *

class LoginFrame(Frame):
    def __init__(self, master=None, caller=None, *args, **kw):

        ## 初始化frame
        Frame.__init__(self, master, bg=values.ROOT_BG_COLOR)

        ## 载入调用函数数据以及控制器
        if (caller==None):
            print("Error: LoginFrame miss caller argument")
            return
        self.caller = caller
        self.controller = getattr(caller, "controller")

        ## 加载UID
        self.uid = 0

        ## UID缓存区
        def limitSizeUID(*args):
            value = self.uidBuffer.get()
            if len(value) > 10: self.uidBuffer.set(value[:10])
        self.uidBuffer = StringVar()
        self.uidBuffer.trace('w', limitSizeUID)

        ## 构建页面
        self.add_widgets()

        ## 载入历史记录
        self.load_historic_uid()

    def add_widgets(self):
        ## 控制界面
        self.control_panel = Frame(self, bg=values.ROOT_BG_COLOR, width=300)
        self.control_panel.pack(fill=Y, expand=False, side=RIGHT)

        ## 相机界面
        self.camera_panel = Label(self, bg=values.CAMERA_BG_COLOR, borderwidth=0)
        #self.camera_panel.place(relx=0, rely=0.5, relwidth=0.7, relheight=1, anchor=W)
        self.camera_panel.pack(fill=BOTH, expand=True, side=RIGHT)
        ## 相机界面图片
        self.img_camera_loading = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"camera_loading.png"}'))
        self.img_camera_disconnected =PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"camera_disconnected.png"}'))
        ## 相机界面初始图片
        self.camera_panel.config(image=self.img_camera_disconnected)

        ## 校徽图标
        self.img_login_page_logo = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"login_page_logo.png"}'))
        self.logo = Label(self.control_panel, image=self.img_login_page_logo, borderwidth=0)
        #self.logo.place(relx=0.5, rely=0, anchor=N)
        self.logo.pack(fill=X, expand=False, side=TOP)

        ## 输入面板
        self.input_panel = Frame(master=self.control_panel, bg=values.ROOT_BG_COLOR)
        #self.input_panel.place(relx=0.5, rely=0.5, relwidth=0.65, anchor=N)
        self.input_panel.pack(fill=X, expand=False, side=TOP, padx=50, pady=(10, 0))

        ## 输入指引
        self.uid_label = Label(master=self.input_panel, borderwidth=0, bg=values.ROOT_BG_COLOR, text="UID:", anchor=W)
        self.uid_label.pack(fill=X, expand=True, side=TOP, pady=10)

        ## UID输入框
        self.uid_entry = Entry(master=self.input_panel, borderwidth=3, relief=FLAT, textvariable=self.uidBuffer)
        self.uid_entry.pack(fill=X, expand=True, side=TOP)
        self.uid_entry.bind("<KeyRelease-Return>", lambda e: self.button_login.invoke())
        self.uid_entry.focus_set()

        ## 提示框
        self.warning_panel = Label(master=self.input_panel, borderwidth=3, relief=FLAT, height=1, bg=values.ROOT_BG_COLOR, fg=values.WARNING_FG_COLOR, anchor=W)
        self.warning_panel.pack(fill=X, expand=True, side=TOP, pady=10)

        ## 登录按钮
        self.img_login = PhotoImage(file = self.get_resource_path(f'{"res"}{os.sep}{"drawable"}{os.sep}{"login.png"}'))
        self.button_login = Button(master=self.control_panel, image=self.img_login, bg=values.ROOT_BG_COLOR, activebackground=values.ROOT_BG_COLOR, border=0)
        self.button_login.configure(command=self.login)
        #self.button_login.place(relx=0.5, rely=0.75, anchor=N)
        self.button_login.pack(fill=X, expand=False, side=BOTTOM, padx=50, pady=(0, 80))
        self.button_login.bind("<Button-3>", (lambda e: self.destroy()))

    def load_historic_uid(self):
        ## 载入历史记录
        if os.path.exists(self.get_resource_path(f'{"res"}{os.sep}{"data"}{os.sep}{"login_record.txt"}')):
            fin = open(self.get_resource_path(f'{"res"}{os.sep}{"data"}{os.sep}{"login_record.txt"}'), 'r', encoding='UTF-8')
            self.uid = fin.read()
            fin.close()
            self.uidBuffer.set(self.uid)
            self.uid_entry.icursor(END)

    def save_historic_uid(self):
        fout = open(self.get_resource_path(f'{"res"}{os.sep}{"data"}{os.sep}{"login_record.txt"}'), 'w', encoding='UTF-8')
        fout.write(str(self.uid))
        fout.close()

    def login(self, event=0):
        self.uid = str(self.uid_entry.get())
        if (self.uid.isdigit() and len(self.uid)==10 and self.verify_uid(int(self.uid))==True):
            self.button_login["state"] = DISABLED
            self.uid_entry.config(state=DISABLED)
            thread = threading.Thread(target=self.turn_on_camera, args=())
            thread.start()
            self.warning_panel.configure(text="")
        elif (not self.uid.isdigit() or len(self.uid)!=10):
            self.warning_panel.configure(text="Invalid Input")
        else:
            self.warning_panel.configure(text="No Such UID")

    def turn_on_camera(self):
        self.camera_panel.config(image=self.img_camera_loading)
        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.face_cascade = cv2.CascadeClassifier(self.get_resource_path(f'{"res"}{os.sep}{"haarcascades"}{os.sep}{"haarcascade_frontalface_default.xml"}'))
        self.video_loop()
        return

    def video_loop(self):
        ## 从摄像头读取照片
        success, img = self.camera.read()
        if success:
            cv2.waitKey(10)
            raw_data = numpy.copy(img)
            ## 转换颜色从BGR到灰阶图
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ## 设定面部识别参数
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
            )
            ## 根据面部识别圈出正方形
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            ## 导出图片  # 转换颜色从BGR到RGBA
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            ## 将图片转换为Image对象
            current_image = Image.fromarray(cv2image)
            ## 对图片大小进行调整
            width, height = current_image.size
            imgtk = ImageTk.PhotoImage(image=self.resize(width, height,  self.camera_panel.winfo_width(), self.camera_panel.winfo_height(), current_image))
            ## 将图片输出到屏幕
            self.camera_panel.imgtk = imgtk
            self.camera_panel.config(image=imgtk)
            ## 进行人脸识别
            if (self.verify_face(raw_data)):
                self.save_historic_uid()
                self.uid_entry.config(state=NORMAL)
                self.button_login["state"] = NORMAL
                self.login_success()
                return
            ## 重新进入循环
            self.after(10, self.video_loop)

    def login_success(self):
        self.controller.post_last_login_time()
        self.caller.click_listener_of_button_home()
        self.destroy_page()
        a = WelcomeTopBar(master=self.caller.root)

    def destroy_page(self):
        self.camera.release()
        cv2.destroyAllWindows()
        self.camera_panel.config(image=self.img_camera_disconnected)
        self.destroy()


    def verify_uid(self, uid):
        return self.controller.check_student_id_in_database(uid)

    def verify_face(self, img_array):
        return self.controller.check_image_pass_face_recognition(img_array)

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
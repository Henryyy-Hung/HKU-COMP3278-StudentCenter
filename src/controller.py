from datetime import *

count = 0

class Controller(object):

    # init the class variable
    def __init__(self):
        # 这玩意初始值是负数，方便识别，不要改它
        self.student_id = -1
        self.email = "demo@connect.hku.hk"

        pass

    # To check whether the 10-digit student ID is exist in the database.
    # If the uid is in database, we assume login will then perform.
    # Thus, if exist, record the Student ID in the $(self.student_id) !!!!!!
    # @param student_id - A 10-digit int type student ID provided by user
    # @return True - The 10-digit student ID is exist in database
    # @return False - The 10-digit student ID is not exist in database
    def check_student_id_in_database(self, student_id):
        state = True # request to database and get it by yourself.
        if (state==True):
            self.student_id = student_id
            print(f'{"check_student_id_in_database":60.60}{state}')
            return True
        else:
            return False

    # To check whether the face match the one in the database
    # use $(self.student_id) to locate which student, and compare student's face and the argument
    # @param img_array - A numpy array which contains the raw data of camera capture. Can use cv to decode.
    # @return True - The img_array match the face of $(self.student_id)
    # @return False - The img_array does not match the face of $(self.student_id)
    def check_image_pass_face_recognition(self, img_array):
        output = False
        global count
        if (count<15):
            count += 1
            output = False
            return output
        output = True
        print(f'{"check_image_pass_face_recognition":60.60}{output}')
        return output

    # To check whether there is a course within 1 hour for the student with $(self.student_id)
    # @return True - There is a course within 1 hour for the student with $(self.student_id)
    # @return False - There isn't a course within 1 hour for the student with $(self.student_id)
    def check_existence_of_course_within_one_hour(self):
        output = False
        print(f'{"check_existence_of_course_within_one_hour":60.60}{output}')
        return output

    # use $(self.student_id) to get student name.
    # @return student_name - A string type student name that belongs to $(self.student_id)
    def get_student_name(self):
        student_name = "Henry Hung"
        print(f'{"get_student_name":60.60}{student_name}')
        return student_name

    # use $(self.student_id) to get student id. <- this function no need to modify!
    # @return str(self.student_id) - A string type student id.
    def get_student_id(self):
        print(f'{"get_student_id":60.60}{self.student_id}')
        return str(self.student_id)

    # use $(self.student_id) to get student last login time.
    # @return student_name - A string type student name that belongs to $(self.student_id)
    def get_student_last_login_time(self):
        ## follow this format to show time thanks
        last_login_time = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day} {datetime.now().hour}:{datetime.now().minute:02}:{datetime.now().second:02}"
        print(f'{"get_student_last_login_time":60.60}{last_login_time}')
        return last_login_time

    # use $(self.student_id) to get the course code of student's next course
    # @return course_code - A string type course_code
    def get_next_course_course_id(self):
        course_id = "COMP3278_A_1st_2022"
        print(f'{"get_next_course_course_id":60.60}{course_id}')
        return course_id

    # 该学生的所有课程。懒得写注释了
    def get_all_courses_course_id(self):
        course_ids = ["CCGL9063_A_1st_2022", "COMP3230_A_1st_2022", "COMP3278_A_1st_2022", "COMP3330_A_1st_2022", "FINA1310_B_1st_2022"]
        print(f'{"get_all_courses_course_id":60.60}{course_ids}')
        return course_ids

    # use $(self.student_id) to get the course_name of student's next course
    # @return course_name - A string type course_name
    def get_course_code_by_course_id(self, course_id):
        course_code = list(course_id.split("_"))[0]
        print(f'{"get_course_code_by_course_id: "+course_id:60.60}{course_code}')
        return course_code

    # use $(self.student_id) to get the course_name of student's next course
    # @return course_name - A string type course_name
    def get_course_name_by_course_id(self, course_id):
        course_name = ""
        if (course_id == "CCGL9063_A_1st_2022"):
            course_name = "How to Make (Sense of) Money"
        elif (course_id == "COMP3230_A_1st_2022"):
            course_name = "Principles of operating systems"
        elif (course_id == "COMP3278_A_1st_2022"):
            course_name = "Introduction to database management systems"
        elif (course_id == "COMP3330_A_1st_2022"):
            course_name = "Interactive Mobile Application Design and Programming"
        elif (course_id == "FINA1310_B_1st_2022"):
            course_name = "Corporate finance"
        print(f'{"get_course_name_by_course_id: "+course_id:60.60}{course_name}')
        return course_name

    # use $(self.student_id) to get the subclass of student's next course
    # @return subclass - A string type subclass
    def get_subclass_by_course_id(self, course_id):
        subclass = list(course_id.split("_"))[2][0] + list(course_id.split("_"))[1]
        print(f'{"get_subclass_by_course_id: "+course_id:60.60}{subclass}')
        return subclass

    # use $(self.student_id) to get the venue of student's next course
    # @return venue - A string type venue
    def get_venue_by_course_id(self, course_id):
        venue = ""
        if (course_id == "CCGL9063_A_1st_2022"):
            venue = "MWT1"
        elif (course_id == "COMP3230_A_1st_2022"):
            venue = "LG.01"
        elif (course_id == "COMP3278_A_1st_2022"):
            venue = "MWT2"
        elif (course_id == "COMP3330_A_1st_2022"):
            venue = "LE4"
        elif (course_id == "FINA1310_B_1st_2022"):
            venue = "KK202"
        print(f'{"get_venue_by_course_id: "+course_id:60.60}{venue}')
        return venue

    # use $(self.student_id) to get the lecturer(s) of student's next course
    # @return lecturer - A string type lecturer(s)
    def get_lecturer_by_course_id(self, course_id):
        lecturer = ""
        if (course_id == "CCGL9063_A_1st_2022"):
            lecturer = "Prof. McDonald,Tom"
        elif (course_id == "COMP3230_A_1st_2022"):
            lecturer = "Prof. Wu,Chenshu"
        elif (course_id == "COMP3278_A_1st_2022"):
            lecturer = "Prof. Luo,Ping"
        elif (course_id == "COMP3330_A_1st_2022"):
            lecturer = "Prof. Chim,Tat Wing"
        elif (course_id == "FINA1310_B_1st_2022"):
            lecturer = "Prof. Huang,Jiantao"
        print(f'{"get_lecturer_by_course_id: "+course_id:60.60}{lecturer}')
        return lecturer

    # use $(self.student_id) to get the message post by lecturer(s) and TA(s) of student's next course
    # @return messages - A array consists of tuples, each tuple contains ((str) job title, (str) name of sender, (str) message)
    def get_messages_by_course_id(self, course_id):
        messages = list()
        if (course_id == "CCGL9063_A_1st_2022"):
            messages = [("Professor", "Mcdonald Tom", "Call for research participants — Do you own NFTs?"),
                        ("Professor", "Mcdonald Tom", "(16 Nov class) Watch party + Letter writing exercise Q&A"),
                        ("Professor", "Mcdonald Tom", "Hong Kong Money Museum exhibit — grades and feedback"),
                        ("Professor", "Mcdonald Tom", "Class Arrangements during Bad Weather"),
                        ("Professor", "Mcdonald Tom", "14 Sep 2022 lecture – Mock quiz"),
                        ]
        elif (course_id == "COMP3230_A_1st_2022"):
            messages = [("TA", "Zhang Xie", "summary of the mid-term exam"),
                        ("Professor", "Wu Chenshu", "Midterm & Problem Set #3"),
                        ("Professor", "Wu Chenshu", "mid-term grades"),
                        ("TA", "Zhang Xie", "Grade of Problem Set #2 is release"),
                        ("Professor", "Wu Chenshu", "Midterm on Oct 27, Thursday"),
                        ("TA", "Zhang Xie", "Arrangement of Tomorrow's Course [Oct 25, Tue]"),
                        ("Professor", "Wu Chenshu", "Amendment to Problem-Set #2"),

                        ]
        elif (course_id == "COMP3278_A_1st_2022"):
            messages = [("Professor", "Ping Luo", "More explanations of Course Materials"),
                       ("Professor", "Ping Luo", "Uploaded MySQL installation"),
                       ("Professor", "Ping Luo", "Assignment 2 has been released!"),
                       ("Professor", "Ping Luo", "SQL Challenge Score released"),
                       ("TA", "Yao Mu", "Notice of Assignment1"),
                       ("TA", "Yao Mu", "SQL Challenge Preparation Submission Link reopened"),
                       ("TA", "Yao Lai", "SQL Challenge"),
                       ("TA", "Yizhou Li", "project groups has been set up in moodle"),
                       ("TA", "Yizhou Li", "Hello World"),
                       ]
        print(f'{"get_messages_by_course_id: "+course_id:60.60}')
        return messages

    # use $(self.student_id) to get the zoom links of student's next course
    # @return zoom_links - A array consists of tuples, each tuple contains ((str) name of link, (str) url of zoom link)
    def get_zoom_links_by_course_id(self, course_id):
        zoom_links = [("Tuesday Class", "https://hku.zoom.us/j/96226740999?pwd=ZER1UUdxSVVhQzNXbXFkUDd3WjRBdz09"),
                      ("Friday Class", "https://hku.zoom.us/j/96226740999?pwd=ZER1UUdxSVVhQzNXbXFkUDd3WjRBdz09"),
                      ("Tutorial Class", "https://hku.zoom.us/j/96226740999?pwd=ZER1UUdxSVVhQzNXbXFkUDd3WjRBdz09")
                      ]
        print(f'{"get_zoom_links_by_course_id: "+course_id:60.60}{zoom_links[0]}')
        return zoom_links

    # use $(self.student_id) to get the materials of student's next course
    # @return zoom_links - A array consists of tuples, each tuple contains ((str) category of material, (str) name of material, (str) url of material)
    def get_materials_by_course_id(self, course_id):
        materials = [("Lectures", "Lecture 1 intro to DBMS", "https://moodle.hku.hk/mod/resource/view.php?id=2665229"),
                    ("Lectures", "Lecture 2 Entity-Relationship Modeling","https://moodle.hku.hk/mod/resource/view.php?id=2665229"),
                    ("Lectures", "Lecture 3 ER Design","https://moodle.hku.hk/mod/resource/view.php?id=2665229"),
                    ("Lectures", "Lecture 4 SQL","https://moodle.hku.hk/mod/resource/view.php?id=2665229"),
                    ("Lectures", "Lecture 5 SQL_II", "https://moodle.hku.hk/mod/resource/view.php?id=2665229"),
                    ("Assignment", "assignment_1.pdf", "https://moodle.hku.hk/mod/resource/view.php?id=2665229"),
                     ]
        print(f'{"get_zoom_links_by_course_id: "+course_id:60.60}{materials[0]}')
        return materials

    # 使用 $(self.student_id) 和 函数参数 $(days_of_the_week) 来锁定指定的学生和指定的7个日子（从周一到周日）
    # 接着从服务器获取这7个日子内，该学生所有的time slots。
    # 输出格式为一个list, list里包含n个tuple，每个tuple包含3个数据，依次为course code, weekday, starting time, ending time。
    # weekday 为 1-7， 1代表周一，7代表周日
    # starting time 不得超过 ending time
    # starting time 和 ending time 都应该大于等于0， 小于等于24
    # 两个time slot不应该出现重叠
    # @param days_of_the_week 一个包含了7个datetime.datetime对象的list
    # @return time_slots - A array consists of tuples, each tuple contains ((str) course code, (int) week day, (float) start time, (float) end time)
    def get_time_slots_of_the_week(self, days_of_the_week):
        ## 使用days of the week
        time_slots = [("COMP3278", 1, 12.5, 14.5),
                      ("COMP3330", 1, 14.5, 16.5),
                      ("COMP3230", 2, 10.5, 12.5),
                      ("FINA1310", 3, 9.5, 12.5),
                      ("CCGL9063", 3, 14.5, 17.5),
                      ("COMP3230", 4, 12.5, 14.5),
                      ("COMP3278", 4, 15.5, 17.5),
                      ("COMP3330", 5, 12.5, 14.5),
                      ]

        print(f'{"get_time_slots_of_the_week":60.60}{time_slots[0]}')
        return time_slots

    # use $(self.student_id) to get the login_records of student
    # @return records - A array consists of tuples, each tuple contains ((str) login time, (str) logout time, (str) duration)
    def get_login_records(self):
        records = [("2022-10-1 10:15", "2022-10-1 16:33", "6 hour"),
                        ("2022-10-2 11:21", "2022-10-2 11:13", "0.5 hour"),
                        ("2022-10-3 15:33", "2022-10-3 16:33", "1 hour"),
                        ("2022-10-14 16:00", "2022-10-14 17:15", "1.3 hour"),
                        ("2022-10-15 09:00", "2022-10-15 09:30", "0.5 hour"),
                        ("2022-10-26 11:20", "2022-10-26 11:50", "0.5 hour"),
                        ("2022-10-28 20:30", "2022-10-28 21:30", "1 hour"),
                        ("2022-11-11 11:20", "2022-11-11 11:50", "0.5 hour"),
                        ("2022-11-20 15:30", "2022-11-20 16:33", "1 hour"),
                        ]
        print(f'{"get_login_records":60.60}{records[0]}')
        return records

    def get_student_email(self):
        student_email = self.email
        print(f'{"get_login_records":60.60}{student_email}')
        return student_email

    # update the student email address in the database
    def post_new_student_email(self, new_student_email_address):
        # post new email
        self.email = new_student_email_address
        print(f'{"post_new_student_email":60.60}{new_student_email_address}')

    # post the last login time to the database
    def post_last_login_time(self):
        last_login_time = str(datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second))
        ## post last_login_time to the server
        print(f'{"post_last_login_time":60.60}{last_login_time}')

    # post the last logout time to the database
    def post_last_logout_time(self):
        last_logout_time = str(datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second))
        print(f'{"post_last_logout_time":60.60}{last_logout_time}')
        ## 此处应该清空controller内所有缓存数据

    # 从服务器获取关于下一节课的所有相关资料，从服务器获取当前用户的邮箱，将所有信息整合好，发送到用户邮箱。
    def send_email_regarding_course_info_by_course_id(self, course_id):
        print(f'{"send_email_regarding_course_info_by_course_id":60.60}{course_id}')




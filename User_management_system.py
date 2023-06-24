# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import tkinter as tk
from tkinter import messagebox as tkMessageBox
import pymysql # 连接mysql用
import tkinter.messagebox




# 连接mysql
conn = pymysql.connect(host='127.0.0.1', user='root', password='123456')
# 获取连接的游标
cur = conn.cursor()

# 执行语句,创建数据库Test
SQL_command = 'create database if not exists test'
cur.execute(SQL_command)
conn.commit()

# 执行语句,展示所有数据库
cur.execute('show databases')
# 遍历所有数据库 (多维元组)
for i in cur:
    print(i)



# 用户管理界面
def make_window(theme):
    sg.theme(theme)
    # 菜单栏
    menu_def = [['Help', ['About...', ['你好']]], ]
    # 连接mysql
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='test', charset='UTF8MB4')
    cur = conn.cursor()


    # Sql命令，创建一个表命名user_ 表里面包含id name tel等表头
    sql1 = ''' create table if not exists users_(id char(100) primary key,
                                                        name char(20) not null,
                                                        sex char(2) not null,
                                                        tel char(100) not null,
                                                        psd char(100))engine=innodb default charset=UTF8MB4;'''
    # 执行SQL1命令
    cur.execute(sql1)
    conn.commit()

    # 用户管理界面
    def user_data():
        # 从users_表里面拿出id name 等信息
        sql = 'select id,name,sex,tel,"****"as psd from users_'
        cur.execute(sql)

        data = []
        # 遍历 逐行读取
        for all in cur.fetchall():
            a = str(all[0])
            b = str(all[1])
            c = str(all[2])
            d = str(all[3])
            data1 = [a,b,c,d]
            data.append(data1)
        # 表头
        headings = ['用户ID','姓名','性别','电话']
        return data,headings

    layout = [[sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
              [sg.Text('用户管理系统', size=(50, 1), justification='center', font=("Helvetica", 16),
                       relief=sg.RELIEF_RIDGE, key='-TEXT HEADING-',expand_x=True)],
              # 创建表格界面
              [sg.Table(values=user_data()[0], headings=user_data()[1],
                        # 最大列宽30
                        max_col_width=30,
                        # 适应列宽
                        auto_size_columns=True,
                        # 不显示编号
                        display_row_numbers=False,
                        # 居中显示
                        justification='center',
                        # 20行
                        num_rows=20,
                        key='-TABLE_user-',
                        # 选中行的时候标黄
                        selected_row_colors='red on yellow',
                        enable_events=True,
                        expand_x=True,
                        expand_y=True,
                        vertical_scroll_only=False,
                        enable_click_events=True,  # Comment out to not enable header and other clicks

                        )],
              # enable_events事件属性
              [sg.Text('用户ID:'), sg.Input(s=(8, 1), enable_events=True, key='-IN_ID-'),
               sg.Text('姓名:'), sg.Input(s=(8, 1), enable_events=True, key='-IN_nam-'),
               sg.Text('性别:'), sg.Input(s=(4, 1), enable_events=True, key='-IN_sex-'),
               sg.Text('电话:'), sg.Input(s=(12, 1), enable_events=True, key='-IN_NUM-'),
               sg.Text('密码:'), sg.Input(s=(9, 1), enable_events=True, key='-IN_psw-')],
              [sg.Button('添加'), sg.Button('查询'), sg.Button('修改'), sg.Button('删除')],
              [sg.Text('添加：依次输入用户ID、姓名、性别、电话、密码')],
              [sg.Text('查询：按照用户ID进行查询')],
              [sg.Text('修改：依次输入用户信息，将原信息修改为先信息')],
              [sg.Text('删除：删除选中的信息')],
              [sg.Sizegrip()]
              ]
    window = sg.Window('用户管理系统', layout)


    while True:
        # 添加事件，与上面的操作对应起来
        event, values = window.read(timeout=100)

        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break
        elif event == '修改':
            # values['-IN_ID-']是从上面的界面中拿数据
            newuser = [values['-IN_ID-'], values['-IN_nam-'], values['-IN_sex-'], values['-IN_NUM-'],
                       values['-IN_psw-']]
            # 写SQL命令，将新数据对数据库做更新
            sql1 = 'select id from users_'
            sql2 = 'update users_ set name=%s where id=%s'
            sql3 = 'update users_ set sex=%s where id=%s'
            sql4 = 'update users_ set tel=%s where id=%s'
            sql5 = 'update users_ set psd=%s where id=%s'

            # 判断学生是否存在
            cur.execute(sql1)
            select_id = cur.fetchall()
            for i in select_id:
                if int(values['-IN_ID-']) == int(i[0]):
                    cur.execute(sql2, (newuser[1], values['-IN_ID-']))
                    conn.commit()
                    cur.execute(sql3, (newuser[2], values['-IN_ID-']))
                    conn.commit()
                    cur.execute(sql4, (newuser[3], values['-IN_ID-']))
                    conn.commit()
                    cur.execute(sql5, (newuser[4], values['-IN_ID-']))
                    conn.commit()
                    break

            else:
                conn.rollback()
            window["-TABLE_user-"].update(values=user_data()[0])

        elif event == '添加':
            newuser = [values['-IN_ID-'],values['-IN_nam-'],values['-IN_sex-'],values['-IN_NUM-'],values['-IN_psw-']]

            try:
                # 为数据库中插入数据
                sql6 = 'insert into users_(id,name,sex,tel,psd) values(%s,%s,%s,%s,%s)'
                cur.execute(sql6, (int(newuser[0]), newuser[1], newuser[2], newuser[3], newuser[4]))
                conn.commit()
                print('添加成功')

            except Exception as e:
                # 回滚
                conn.rollback()
                print('添加失败，该用户ID存在')
            window["-TABLE_user-"].update(values=user_data()[0])



        elif event == '删除':
            newuser = [values['-IN_ID-'], values['-IN_nam-'], values['-IN_sex-'], values['-IN_NUM-'],
                       values['-IN_psw-']]
            # 删除命令
            sql1 = 'delete from users_ where id=%s'
            # 判断学生是否存在
            sql2 = 'select id from users_'
            cur.execute(sql2)
            select_id = cur.fetchall()
            for i in select_id:

                # 以ID为判别指标 不用姓名 姓名可能重复 ID唯一
                if int(newuser[0]) == int(i[0]):
                    cur.execute(sql1, (newuser[0],))
                    conn.commit()
                    break
            else:
                conn.rollback()
            window["-TABLE_user-"].update(values=user_data()[0])

        elif event == '查询':
            newuser = [values['-IN_ID-'], values['-IN_nam-'], values['-IN_sex-'], values['-IN_NUM-'],
                       values['-IN_psw-']]

            # 判断学生是否存在
            sql2 = 'select id,name,sex,tel from users_'
            cur.execute(sql2)
            select_id = cur.fetchall()
            data2 = []
            for i in select_id:

                if int(newuser[0]) == int(i[0]):
                    a = str(i[0])
                    b = str(i[1])
                    c = str(i[2])
                    d = str(i[3])
                    data1 = [a, b, c, d]
                    data2.append(data1)
                    break
            else:
                conn.rollback()
            window["-TABLE_user-"].update(values=data2)

    window.close()
    exit(0)


# 用户注册界面
def Registration():


    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='test', charset='UTF8MB4')
    cur = conn.cursor()

    # 创建表
    sql1 = ''' create table if not exists users_(id char(100) primary key,
                                                name char(20) not null,
                                                sex char(2) not null,
                                                tel char(100) not null,
                                                psd char(100))engine=innodb default charset=UTF8MB4;'''
    # doSQL()
    cur.execute(sql1)
    conn.commit()

    # 定义添加函数
    def insert_105():
        # 定义一个弹窗
        a = tk.messagebox.askquestion(title='提示窗', message='你确定要添加么？')
        if a == 'yes':
            try:
                sql2 = 'insert into users_(id,name,sex,tel,psd) values(%s,%s,%s,%s,%s)'
                cur.execute(sql2, (int(id.get()), name.get(), sex.get(), tel.get(), psd.get()))
                conn.commit()
                tk.messagebox.showinfo(title='提示窗', message='添加成功')
                print('添加成功')

            except Exception as e:
                # 回滚
                conn.rollback()
                print('添加失败，该用户ID存在')
                tk.messagebox.showinfo(title='提示窗', message='添加失败，该用户ID存在')
            # clear_105()
    # 定义退出函数 退出后本窗口关闭 进入登录界面
    def exit_105():
        a = tk.messagebox.askquestion(title='提示窗', message='你真的要退出么？')
        if a == 'yes':
            window.destroy()
            Sign_in()
    # 定义关于弹窗
    def about_105():
        tk.messagebox.showinfo(title='关于', message='xxx')

    # 创建窗口
    window = tk.Tk()
    window.title('用户注册')
    window.geometry('600x380+480+135')
    # 菜单栏
    menubar = tk.Menu(window)

    menubar.add_cascade(label='关于', command=about_105)
    window.config(menu=menubar)
    # 主界面
    # 用户ID
    tk.Label(window, text='用户ID:', font=("微软雅黑", 10, "bold", "italic")).place(x=25, y=25)
    id = tk.Entry(window, width=20, borderwidth=3)
    id.place(x=75, y=25)
    # 姓名
    tk.Label(window, text='姓名:', font=("微软雅黑", 10, "bold", "italic")).place(x=230, y=25)
    name = tk.Entry(window, width=20, borderwidth=3)
    name.place(x=280, y=25)
    # 性别
    tk.Label(window, text='性别:', font=("微软雅黑", 10, "bold", "italic")).place(x=435, y=25)
    sex = tk.Entry(window, width=10, borderwidth=3)
    sex.place(x=485, y=25)
    # 电话
    tk.Label(window, text='电话:', font=("微软雅黑", 10, "bold", "italic")).place(x=25, y=75)
    tel = tk.Entry(window, width=20, borderwidth=3)
    tel.place(x=75, y=75)
    # 地址
    tk.Label(window, text='密码:', font=("微软雅黑", 10, "bold", "italic")).place(x=230, y=75)
    psd = tk.Entry(window, width=39, borderwidth=3)
    psd.place(x=280, y=75)
    # 添加按钮
    tk.Button(window, text='添加', bd=5, width=5, height=1, command=insert_105).place(x=50, y=130)
    # 添加退出
    tk.Button(window, text='退出', bd=5, width=5, height=1, command=exit_105).place(x=500, y=130)


    tk.mainloop()
    cur.close()
    conn.close()

# 用户登录界面
def Sign_in():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='test', charset='UTF8MB4')
    cur = conn.cursor()
    sql2 = 'select id,psd from users_'

    # 登录时输入密码事件
    def handler():
        username = entry.get()
        password = entry2.get()
        if username == '' and password == '':
            tkMessageBox.showinfo('警告', '账号和密码不能为空')
        elif username == '' and password != '':
            tkMessageBox.showinfo('警告', '账号不能为空')
        elif username != '' and password == '':
            tkMessageBox.showinfo('警告', '密码不能为空')
        else:
            # 判断学生是否存在
            cur.execute(sql2)
            select_id = cur.fetchall()
            # 拿到ID
            i_ = []
            for i in select_id:
                if int(username) == int(i[0])and password == i[1]:
                    window0.destroy()
                    make_window(sg.theme())
                i_.append(int(i[0]))
            if int(username) not in i_:
                a = tk.messagebox.askquestion(title='提示窗', message='请先注册')
                if a == 'yes':
                    pass


    def handler1():
        window0.destroy()
        Registration()

    # 登录界面的功能及分布
    # 从这开始到最后一行都是登录界面的插件类型及功能的设置
    window0 = tk.Tk()
    window0.title('用户管理系统')
    window0.geometry('600x300')
    window0.resizable(False, False)

    frame1 = tk.Frame(window0)
    frame2 = tk.Frame(window0)
    frame3 = tk.Frame(window0)
    frame4 = tk.Frame(window0)
    userNameLabel = tk.Label(frame1, text="账号：", fg='green')
    userNameLabel.pack(side=tk.LEFT)
    passWordLabel = tk.Label(frame2, text="密码：", fg='green')
    passWordLabel.pack(side=tk.LEFT)
    entry = tk.Entry(frame1)
    entry.pack(side=tk.RIGHT)
    entry2 = tk.Entry(frame2, show='*')
    entry2.pack(side=tk.RIGHT)
    btn = tk.Button(frame3, text=u'安全登录', command=handler, fg='blue')
    btn.pack(side=tk.BOTTOM)
    btn = tk.Button(frame4, text=u'用户注册', command=handler1, fg='blue')
    btn.pack(side=tk.BOTTOM)
    Exp = tk.Label(master=window0)
    Exp.pack(side=tk.BOTTOM)
    frame1.pack(fill=tk.Y, expand=tk.YES)
    frame2.pack(fill=tk.Y, expand=tk.NO)
    frame3.pack(fill=tk.NONE, expand=tk.YES)
    frame4.pack(fill=tk.NONE, expand=tk.NO)
    window0.mainloop()

if __name__ == '__main__':
    Sign_in()
    Sign_in()
    # make_window(sg.theme())

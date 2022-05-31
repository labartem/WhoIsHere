import clipboard
import Esi
import time
import User_base
import Conf_pars
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Canvas
from tkinter import PhotoImage
from tkinter import Frame
from tkinter import StringVar
from threading import Thread
from pynput import keyboard
import threading
import os


class Table(tk.Frame):
    def __init__(self, parent=None, rows=tuple()):
        super().__init__(parent)
        print("start table")
        dir_path = "%s\\WhoIsHere\\" %os.environ['APPDATA']
        read_conf_param = Conf_pars.read_con_file(dir_path)
        columns = ('Nickname','Corporation','Alliance','Sec status','Ship Kill','Solo Kill','Ship Lost','Gang Ratio')
        self.table =  ttk.Treeview(self, columns = columns, show='headings')
        for col in columns:
            self.table.heading(col,text=col,command=lambda c=col: self.treeview_sort_column(self.table, c,True))
            self.table.column(col,width=120)

        for row in rows:
            self.table.insert('', tk.END, values=tuple(row))

        mainmenu = tk.Menu(self)
        root.config(menu=mainmenu)
        root.resizable(width=False, height=False)
        configmenu = tk.Menu(mainmenu,tearoff=0)
        configmenu.add_command(label="Filter",command = self.filter_window)

        self.show_top = tk.BooleanVar()
        self.show_top.set(read_conf_param[0][1])
        self.thread_l_flag = tk.BooleanVar()
        self.thread_l_flag.set(read_conf_param[1][1])
        self.check_param(read_conf_param[0][1],read_conf_param[1][1])

        configmenu.add_checkbutton(label='Always  on Top', onvalue= 1,offvalue = 0, variable=self.show_top, command=self.param_always_on_top)
        configmenu.add_checkbutton(label='Background key interception', onvalue= 1,offvalue = 0, variable=self.thread_l_flag, command=self.thread_listener)
        configmenu.add_command(label="Exit",command = self.quit)

        mainmenu.add_cascade(label="Configure", menu = configmenu)
        mainmenu.add_cascade(label="About", command = self.about_window)

        scrolltable = tk.Scrollbar(self, command=self.table.yview)
        self.table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)
        self.c = Canvas(self,width =30,height =30,bg= "white")
        self.button_input = tk.Button(self,text="Input",width = 10,height =2,fg = "black", command = self.enterclipboard)
        self.button_stop = tk.Button(self,text="Stop",width = 10,height =2,fg = "black", command = self.stop_inter_threadself)
        hidden_scale = tk.Scale(self,orient = "horizontal", from_ = 100, to = 20 ,command = self.change_transparency,showvalue = 0)
        self.c.pack(padx = 10,side ='left')
        self.button_input.pack(side ='left')
        self.button_stop.pack(side = 'right')
        hidden_scale.pack(side='right')
        self.label_info = tk.Label(self,text = "XXXXXX",height = 2)
        self.label_info.pack( side='bottom')
        self.click_timer = 0


    def check_param(self,*args):
        if args[0] == 'True':
            print("Start Always on top")
            self.param_always_on_top()
        if args[1] == 'True':
            print("Start listen in background")
            self.thread_listener()
        print("Argument ",args[0])


    def change_transparency(self,value):
        root.attributes('-alpha',int(value)/100)

    def param_always_on_top(self):
        if self.show_top.get():
            root.wm_attributes("-topmost", True)
        else:
            root.wm_attributes("-topmost", False)

    def on_tree_select(self,event):
        self.c.create_oval(3,3,30,30,fill = "red")
        self.c.update()
        self.table.bind('<ButtonPress-1>', self.start_motor )
        self.table.bind('<ButtonRelease-1>',self.stop_motor)

    def start_motor(self,event):
        self.click_timer = time.time()
        print(time.ctime(self.click_timer), " start ")
        print("start", '{0:.2f}'.format(self.click_timer))

    def stop_motor(self,event):
        self.click_timer = time.time() - self.click_timer
        print('{0:.2f}'.format(self.click_timer), " stop")
        if self.click_timer > 2:
            print('Select item: ')
            try:
                url = User_base.user_url_req(self.table.item(self.table.selection())['values'][0])
            except Exception as e:
                url = "https://zkillboard.com/"
                print("Error zkillboard copy  ", e.args[0])

            clipboard.copy(url)
            self.c.create_oval(3,3,30,30,fill = "green")
            self.c.update()
            self.label_info['text'] = "Copied"
            print("self.VIBOR: ",self.click_timer, " Skopirovano")
            self.click_timer = 0

            time.sleep(1)
            self.c.delete("all")
        self.c.delete("all")

    def the_choice_column(self,event):
        if self.table.identify_region(event.x,event.y) == "heading" :
            col = self.table.column(self.table.identify_column(event.x))['id']
            self.treeview_sort_column(self.table,col,reverse = False)

    def treeview_sort_column(self,table, col,reverse):
        l = [(self.table.set(k, col),  k) for k in self.table.get_children()]

        if col == "Ship Kill" or col == "Solo Kill" or col == "Ship Lost" or col == "Gang Ratio":
            l.sort(key=lambda t: int(t[0]),reverse=reverse)
        elif col == "Sec status":
            l.sort(key=lambda t: float(t[0]),reverse=reverse)
        else:
            l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.table.move(k, '', index)

        self.table.heading(col, command=lambda:
                           self.treeview_sort_column(self.table, col, not reverse))

    def enterclipboard(self,event = 0): #
        # Insert information about  users from clipboard
        print("Insert")
        user_pl= []

        for i in clipboard.paste().splitlines():
            user_pl.append(i.strip())
        print("V Copy ", user_pl)
        r = User_base.search_nicknames_in_filter(user_pl)
        user_pl = User_base.search_nicknames_in_filter_user_acc(r)
        if user_pl == []:
            pass
        else:
            self.startTime = time.time()
            self.inter_threadself(user_pl)

    def stop_inter_threadself(self):
        print(threading.active_count())
        print("enumerate: ", threading.enumerate())
        try:
            self.stop_threads = True
            print("Thread is alive: ", self.th.is_alive())
            self.label_info.configure(text = "I'm resting"  )
        except:
            pass

    def inter_threadself(self,user_pl):
        print(user_pl)
        self.th = Thread(target = self.enterdatatable,args = (user_pl,),name = "nick_name")
        self.stop_threads = False
        self.th.start()

    def _onKeyRelease(self,event):
        ctrl  = (event.state & 0x4) != 0
        if event.keycode == 86 and  ctrl and event.keysym.lower() != "v":
            self.enterclipboard()

    def thread_listener(self):
        self.thread_list = Thread(target = self.copy_keylis,name = "key_listener")
        self.thread_list.start()

    def copy_keylis(self):
        print("start listen")
        if self.thread_l_flag.get():
            with keyboard.Listener(on_press=self.listener_press) as listener:
                listener.join()
        else:
            print(threading.active_count())
            print("enumera  te: ", threading.enumerate())
            print("Return False")
            return False

    def listener_press(self,key):
        time.sleep(0.1)
        print(key)
        try:
            if self.thread_l_flag.get():
                if str(key) == r"'\x03'":
                    print('press ctrl+c!')
                    print(clipboard.paste())
                    self.enterclipboard()
            else:
                return False
        except Exception as e:
            print(e.args[0])

    def enterdatatable(self,user_pl):
        #insert in table
        print("data ", user_pl)
        i = 0
        b = []
        z = ()
        o = 0
        i = 0
        L = []

        for i in range(len(user_pl)):
            if self.stop_threads:
                break
            b.append([])
            self.label_info.configure(text = "Processing user information:: " + user_pl[i] + " Remaining to process: " + str(int(len(user_pl)) - i) )
            root.update()
            users =  User_base.search_nicknames(user_pl[i])
            print("LOOOP USERS",users,users[0])
            for l in range(1):
                users[0],users[1],users[2]
                b[i].append(users[0])
                b[i].append(users[1])
                b[i].append(users[2])
                b[i].append(users[3])
                b[i].append(users[4])
                b[i].append(users[5])
                b[i].append(users[6])
                b[i].append(users[7])

        z = b
        rows = z
        for i in self.table.get_children():
            self.table.delete(i)
        for row in rows:
            self.table.insert('', tk.END, values=tuple(row))
        end_time = "Work done for: {:.3} sec".format(time.time() - self.startTime)
        self.label_info.configure(text = end_time)

    def filter_window(self):
        ##create window fot filter player
        self.flag = 1
        print("start_filter")
        filt_window = tk.Toplevel(self,padx = 10, pady = 10)
        filt_window.title("Filter Account")
        filt_window.geometry("560x460")
        filt_window.lift(aboveThis=self)
        filt_window.bind("<Key>", self._onKeyRelease_filt, "+")
        filt_window.resizable(width=False, height=False)
        filt_window.attributes('-topmost', True)
        filt_window.focus_set()
        filt_window.grab_set()
        frame_filter_insert_nick = tk.Frame(filt_window)
        frame_filter_text_info = tk.Frame(filt_window)
        frame_filter_user_nick = tk.Frame(filt_window)
        frame_filter_general_nick = tk.Frame(filt_window)

        label_filt_window = tk.Label(frame_filter_insert_nick,text= "Add user nick for filter",height = 2,width = 25,borderwidth = 1,relief="solid")
        label_filt_window1 = tk.Label(frame_filter_general_nick,text= "In filter",height = 2,width = 10,borderwidth = 1,relief="solid")
        label_filt_window_user_acc_nick = tk.Label(frame_filter_user_nick,text= "My account",height = 2,width = 10,borderwidth = 1,relief="solid")
        self.text_enter_filt_window = tk.Text(frame_filter_insert_nick,height = 5 ,width = 30)
        button_enter_filt_window = tk.Button(frame_filter_insert_nick,text = "Add general user filter", height = 1,width = 20, command = self.copy_list)
        button_add_u_acc_filt_window = tk.Button(frame_filter_insert_nick,text = "Add my acc filter", height = 1,width = 20, command = self.add_u_acc_filter)
        button_clear_filt_window = tk.Button(frame_filter_general_nick,text = "Clear general filter", height = 1,width = 20, command = self.clear_filter_list)
        button_clear_u_acc_filt_window = tk.Button(frame_filter_user_nick,text = "Clear my acc filter", height = 1,width = 20, command = self.clear_u_acc_filter_list)

        j = [x[0] for x in  User_base.get_data_in_filter()]
        self.list_box_nick = tk.Listbox(frame_filter_general_nick, listvariable=StringVar(value=j),width=40)
        k = [x[0] for x in  User_base.get_data_in_u_acc_filter()]
        self.list_box_user_acc_nick = tk.Listbox(frame_filter_user_nick, listvariable=StringVar(value=k ),width=40)
        s_user_acc_filter = tk.Scrollbar(frame_filter_user_nick,orient= 'vertical',command= self.list_box_user_acc_nick.yview)
        self.list_box_user_acc_nick['yscrollcommand'] = s_user_acc_filter.set

        s_general_acc_filter = tk.Scrollbar(frame_filter_general_nick,orient= 'vertical',command= self.list_box_nick.yview)
        self.list_box_nick['yscrollcommand'] = s_general_acc_filter.set


        label_txt_img = tk.Label(frame_filter_text_info,height = 11,width = 28, font="Arial 12")
        label_txt_img['text'] = """General filter\n You can add all the nicknames \n of the players you need to this filter,
          for example, the players of the \n current fleet.\n
        User character filter(my acc).\n Removes the desired characters
        from the general filter, so as not
        to add them several times."""
        label_filt_window.grid(column = 0, row = 0 ,padx = 5, pady = 2)
        self.text_enter_filt_window.grid(column = 0, row =1,padx = 5, pady = 5)
        label_txt_img.grid(column = 0, row = 0)
        button_enter_filt_window.grid(column = 0, row =2,padx = 5, pady = 2)
        button_add_u_acc_filt_window.grid(column = 0, row =3,padx = 5, pady = 2)
        button_clear_filt_window.grid(column=0,row=6,padx = 5, pady = 2)

        self.list_box_nick.grid(column = 0, row =1)
        s_user_acc_filter.grid(column = 1, row =1,sticky='nse')
        s_general_acc_filter.grid(column = 1, row =1,sticky='nse')
        self.list_box_user_acc_nick.grid(column = 0, row =1)
        label_filt_window_user_acc_nick.grid(column =0 , row =0,padx = 5, pady = 2)
        label_filt_window1.grid(column = 0, row =0,padx = 5, pady = 2)
        button_clear_u_acc_filt_window.grid(column =0 , row = 2,padx = 5, pady = 2)

        frame_filter_insert_nick.grid(column = 0, row =1,padx = 5, pady = 2)
        frame_filter_text_info.grid(column = 1, row =1,padx = 5, pady = 2)
        frame_filter_user_nick.grid(column = 1, row =5,padx = 5, pady = 2)
        frame_filter_general_nick.grid(column = 0, row =5,padx = 5, pady = 2)

    def _onKeyRelease_filt(self,event):
        ctrl  = (event.state & 0x4) != 0
        if event.keycode==86 and  ctrl and event.keysym.lower() != "v":
            print(clipboard.paste())
            event.widget.event_generate("<<Paste>>")
        if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")

    def clear_filter_list(self):
        User_base.delete_data_filter()
        self.list_box_nick.delete(0,'end')

    def clear_u_acc_filter_list(self):
        User_base.delete_data_u_acc_filter()
        self.list_box_user_acc_nick.delete(0,'end')

    def get_data_for_filter(self):
        j = 0.0
        l_u_data =  User_base.get_data_in_filter()
        if l_u_data == []:
            self.list_box_nick.insert('end','')
        else:
            print("User get data",l_u_data)
            print(l_u_data[0][0])
            for i in range(0,len(l_u_data)):
                try:
                    self.list_box_nick.insert('end',l_u_data[i][0])
                except Exception as e:
                    print("Error, can't get data for_filter ",e)
                j += 1
            return l_u_data

    def get_data_for_u_acc_filter(self):
        j = 0.0
        l_u_data =  User_base.get_data_in_u_acc_filter()
        if l_u_data == []:
            self.list_box_nick.insert('end','')
        else:
            print("User get data_acc_filter",l_u_data)
            print(l_u_data[0][0])
            for i in range(0,len(l_u_data)):
                try:
                    self.list_box_user_acc_nick.insert('end',l_u_data[i][0])
                except Exception as e:
                    print("Error, can't get data for_u_acc_filter ",e)
                j += 1
            return l_u_data

    def copy_list(self):
        self.list_box_nick.delete(0,'end')
        x =  self.text_enter_filt_window.get('1.0','end' ).split("\n")
        print("ДО ", x)
        x = list(filter(None,x))
        print("После", x)
        print("y", x)
        x = User_base.search_nicknames_in_filter(x)
        print("Ретурн ", x)
        User_base.insert_nick_in_filter(x)
        self.get_data_for_filter()

    def add_u_acc_filter(self):
        x =  self.text_enter_filt_window.get('1.0','end' ).split("\n")
        print("ДО ", x)
        x = list(filter(None,x))
        print("После", x)
        print("y", x)
        x = User_base.search_nicknames_in_filter_user_acc(x)
        print("Ретурн ", x)
        x = User_base.search_nicknames_in_filter_for_add_user_acc(x)
        print("Xxxxx2 ", x)
        User_base.insert_nick_in_filter_user_acc(x)

        self.list_box_nick.delete(0,'end')
        self.list_box_user_acc_nick.delete(0,'end')
        self.get_data_for_filter()
        self.get_data_for_u_acc_filter()

    def quit(self):
        value = []
        value.append(self.show_top.get())
        value.append(self.thread_l_flag.get())
        print(value)
        self.thread_l_flag = True
        print(threading.active_count())
        print("enumerate: ", threading.enumerate())
        path = "%s\\WhoIsHere\\" %os.environ['APPDATA']
        Conf_pars.save_config_file(path,value)
        i = 0
        for i in range(5):
            print("До выхода: ", i - 5)
        root.destroy()

    def about_window(self):
        print("About")
        about_win = tk.Toplevel()
        about_win.title("About")
        about_win.geometry("750x500")
        about_win.lift(aboveThis=self)
        about_win.grid()
        about_win.focus_set()
        about_win.grab_set()

        license = """
            Created By Molb Sinulf
            The application uses open data from the game Eve Online and the site zKillboard

            Copyright (c) 2022 - Molb Sinulf

            All rights reserved.

            Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
        """
        label_about = tk.Label(about_win,text= license ,font="Arial 12",justify = "center")
        label_about.grid(column = 1,row = 1,padx=2,pady=2)

def check_exist_file():
    dir_path = "%s\\WhoIsHere\\" %os.environ['APPDATA']
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    if not os.path.exists(dir_path+"file_config.ini"):
        Conf_pars.create_conf_file(dir_path)
    else:
        print("File create")
    User_base.create_db()


if __name__ == "__main__":
    check_exist_file()
    root = tk.Tk()
    # root.lift()
    root.title(u'WhoIsHere')
    z = [('Insert data',' Ctrl + V',' Please OFF',' Caps Lock ',"Created by","Molb Sinulf") ]
    # root.tkraise()
    table = Table(root,  rows=z)
    root.protocol("WM_DELETE_WINDOW", table.quit)
    root.bind("<Key>", table._onKeyRelease, "+")
    root.bind('<<TreeviewSelect>>',table.on_tree_select)
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()

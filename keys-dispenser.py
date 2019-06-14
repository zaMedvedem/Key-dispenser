from tkinter import *
import time
import getpass
import threading

root=Tk()
root.title("Keys Dispenser")

username = getpass.getuser()
file1 = 'batch_1.txt'
file2 = 'batch_2.txt'
var = StringVar(root)
log_var = StringVar(root)
log_text = StringVar(root)
#log_text = []
lock = threading.Lock()

class keys_dispenser(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        Label(self, text="Keys Batch").grid(row=0,column=1, sticky=E)
        var.set("batch_1") # initial value
        OptionMenu(self, var, "batch_1", "batch_2").grid(row=0, column=2, columnspan=3, sticky=W+E)
        Button(self, text="Get Key", command=self.get_key, width=10).grid(row=1, column=2, sticky=W)
        Button(self, text="Cancel", command=self.exit, width=10).grid(row=1, column=3, columnspan=2, sticky=W)
        Label(self, text="Key").grid(row=2,column=1, sticky=E)
        self.answer=Entry(self, width=25)
        self.answer.grid(row=2, column=2, columnspan=2, sticky=W)
        Label(self, text="Advanced").grid(row=3,column=1, sticky=E)
        Button(self, text="View Logs", command=self.view_logs, width=10).grid(row=3, column=2, columnspan=2, sticky=W+E+S+N)

    def view_logs(self):
        logs = Toplevel()
        logs.title("Log Records")

        with open("Log-file.txt", "r") as f:

            log_text.set(f.read())
            Label(logs, text="Sort logs by user").grid(row=0,column=1, sticky=W)
            for i in range(len(self.select_user(username))):
                OptionMenu(logs, log_var, *self.select_user(username)).grid(row=0, column=2, sticky=W)
            Button(logs, text="Sort", command=self.logs_query, width=10).grid(row=0, column=3, sticky=W)
            label = Label(logs, textvariable=log_text, anchor=W, justify=LEFT).grid(row=1, column=1, columnspan = 3, sticky=W)
            Button(logs, text="See all logs", command=self.all_logs, width=10).grid(row=2, column=1, sticky=W+E+S+N)
            Button(logs, text="Close Logs", command=logs.destroy, width=10).grid(row=2, column=3, sticky=W+E+S+N)
            log_var.set(username)

    def get_key(self):

        batch_no = file1 if str(var.get()) == "batch_1" else file2

        lock.acquire()
        file = open(batch_no, "r")
        key = file.readline().rstrip()
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        who_is = " - " + username + " - " + date_time + "\n"
        log_data = key + who_is
        log = open("Log-file.txt", "a+")
        log.write(log_data)
        log.close()

        all_lines = file.readlines()
        file = open(batch_no, "w")
        for line in all_lines:
            if line.rstrip() != key:
                file.write(line)
        file.close()

        d = [key[i:i+3] for i in range(0, len(key), 3)]
        display_key = d[0] + " " + d[1] + " " + d[2] + " " + d[3]
        self.answ=str(display_key)
        self.key_display()
        self.select_user(username)
        lock.release()

    def select_user(self,username):
        select_user = [username]
        log = open("Log-file.txt","r")
        log_users = log.readlines()
        for _ in log_users:
            user = _.split(" - ")

            for i in range(len(select_user)):
                if (user[1] != select_user[i]) and (user[1] != select_user[len(select_user)-1]):
                    add_user = user[1]
                    select_user.append(add_user)
                else:
                    break
        select_user = list(dict.fromkeys(select_user))
        log.close()
        return select_user

    def logs_query(self):
        log_line = []
        #add_log_line = []
        log = open("Log-file.txt","r")
        log_users = log.readlines()
        for _ in log_users:
            user = _.split(" - ")
            if user[1] == str(log_var.get()):
                log_line.append(' - '.join(user))
                #add_log_line.append(' - '.join(user))
        log_text.set(''.join(log_line))
        return log_text

    def all_logs(self):
        with open("Log-file.txt", "r") as f:
            log_text.set(f.read())
        return log_text

    def exit(self):
            root.destroy()

    def key_display(self):
        self.answer.delete(0,END)
        self.answer.insert(0,self.answ)

keys_dispenser=keys_dispenser(root)
root.mainloop()

from tkinter import *
import time
import mysql.connector as sql
from tkinter import messagebox
import sys
import random
from cryptography.fernet import Fernet
import struct
sys.path.insert(0,'./assets')

#global variables
results = []
list1 = ['1','2','3','4','5','6','7','8','9','0']
list2 = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
list3 = ['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
list4 = ['!','@','#','$','%','^','&','*','_','-','=','+','<','>','?']
length = random.randint(8,16)
st = []
c_s = 0
c_n = 0
c_l = 0
c_c = 0
c_s_p = 0
c_n_p = 0
c_l = 0
c_c_p = 0
tpw = ''

#global fungtion
def rawbytes(s):
    """Convert a string to raw bytes without encoding"""
    outlist = []
    for cp in s:
        num = ord(cp)
        if num < 255:
            outlist.append(struct.pack('B', num))
        elif num < 65535:
            outlist.append(struct.pack('>H', num))
        else:
            b = (num & 0xFF0000) >> 16
            H = num & 0xFFFF
            outlist.append(struct.pack('>bH', b, H))
    return b''.join(outlist)


with open('assets/dbp.txt','r') as pwdt:
    pwd = pwdt.read()
    pwdt.close()

try:
    conn=sql.connect(host='localhost',user='root',passwd=pwd,database='passwords',charset='utf8')
    cur = conn.cursor()

except Exception as e:
    print("Error : ",e)

def register():

    def rpg():
        global list1
        global list2
        global list3
        global list4
        global length
        global st
        global c_n
        global c_s
        global c_l
        global c_c
        global c_n_p
        global c_s_p
        global c_l_p
        global c_c_p


        c_n = list1[random.randint(0,len(list1)-1)]

        c_s = list2[random.randint(0,len(list2)-1)]

        c_l = list3[random.randint(0,len(list3)-1)]

        c_c = list4[random.randint(0,len(list4)-1)]
        for i in range (length):
            x = random.randint(1,11)
            if x == 1 or x==5 or x==11:
                st.append(list1[random.randint(0,len(list1)-1)])
            elif x == 2 or x==7 or x==6 or x==10:
                st.append(list2[random.randint(0,len(list2)-1)])
            elif x == 3 or x==8 or x==9:
                st.append(list3[random.randint(0,len(list3)-1)])
            elif x == 4:
                st.append(list4[random.randint(0,len(list4)-1)])

        c_n_p = random.randint(0,len(st)-1)
        def c_s_p_d():
            global c_n_p
            c_s_p = random.randint(0,len(st)-1)
            if c_s_p == c_n_p:
                c_s_p_d()
            return c_s_p

        c_s_p = c_s_p_d()

        def c_l_p_d():
            global c_n_p
            global c_s_p
            c_l_p = random.randint(0,len(st)-1)
            if c_l_p == c_n_p:
                c_l_p_d()
            if c_l_p == c_s_p:
                c_l_p_d()
            return c_l_p

        c_l_p = c_l_p_d()

        def c_c_p_d():
            global c_n_p
            global c_s_p
            global c_l_p
            c_c_p = random.randint(0,len(st)-1)
            if c_c_p == c_n_p:
                c_c_p_d()
            if c_c_p == c_s_p:
                c_c_p_d()
            if c_c_p == c_l_p:
                c_c_p_d()
            return c_c_p

        c_c_p = c_c_p_d()

        st[c_n_p] = c_n
        st[c_s_p] = c_s
        st[c_l_p] = c_l
        st[c_c_p] = c_c

        pw = ''

        for i in range (len(st)):
            pw = pw + st[i]

        entry_1_3.insert(END,pw)
        st = []
        pw = ''

    def reg():
        user_name = entry_1_1.get()
        app = entry_1_2.get()
        q_passw = entry_1_3.get()
        te = Fernet(menu.uk)
        w_passw = te.encrypt(q_passw.encode())
        passw = str(w_passw).split("'")[1]

        st = f"insert into user_{menu.u} values('{user_name}','{app}','{passw}')"
        cur.execute(st)
        conn.commit()
        root_1.destroy()

    root_1 = Tk()
    root_1.title("New Entry")
    head_1_1 = Label(root_1, text = "Enter New Password to the database",font=('Helvetica',9,'bold')).grid(row=0)
    text_1_1 = Label(root_1, text = "User Name : ").grid(row=1,sticky = E)
    text_1_2 = Label(root_1, text = "Application : ").grid(row=2,sticky = E)
    text_1_3 = Label(root_1, text = "Password : ").grid(row=3,sticky = E)
    entry_1_1 = Entry(root_1,width = 45)
    entry_1_2 = Entry(root_1,width = 45)
    entry_1_3 = Entry(root_1,width = 45)
    entry_1_1.grid(row=1,column=1,sticky = W)
    entry_1_2.grid(row=2,column=1,sticky = W)
    entry_1_3.grid(row=3,column=1,sticky = W)
    button_1_1 = Button(root_1,text = "Submit",fg='blue',command=reg).grid(row=4,column=1)
    button_1_2 = Button(root_1,text = "Generate Password",fg= 'blue',command=rpg).grid(row=4)
    root_1.mainloop()

def search():
    def sear():
        app = entry_2_1.get()
        u_n = entry_2_2.get()
        st = f"select pw from user_{menu.u} where user_id = '{u_n}' and application = '{app}'"
        cur.execute(st)
        pw = cur.fetchone()
        if pw != None:
            pw = pw[0]
            pw = rawbytes(pw)
            te = Fernet(menu.uk)
            pw = te.decrypt(pw).decode()
            messagebox.showinfo("PASSWORD",f"PASSWORD : {pw} \n for APP : {app} ; USER : {u_n}")
        else:
            messagebox.showinfo("ERROR 404",f"No saved data founf for USER : {u_n} on application : {app}")

    root_2 = Tk()
    root_2.title("Search Password")
    head_2 = Label(root_2, text = "Search saved password").grid(row=0)
    text_2_1 = Label(root_2, text = "Application : ").grid(row=1,sticky=E)
    text_2_2 = Label(root_2, text = "User Name : ").grid(row=2,sticky=E)
    entry_2_1 = Entry(root_2,width = 45)
    entry_2_2 = Entry(root_2,width = 45)
    entry_2_1.grid(row=1,column=1,sticky=W)
    entry_2_2.grid(row=2,column=1,sticky=W)
    button_2_1 = Button(root_2, text = "Search",fg = 'blue',command=sear).grid(row=3,column=1)
    root_2.mainloop()

def delete():
    user = menu.u
    if messagebox.askokcancel("DELETE USER","Are you sure you want to delete the user? all stored passwords will be lost forever."):
        cur.execute(f"drop table user_{user}")
        conn.commit()
        cur.execute(f"delete from log_id where user_id = '{user}'")
        conn.commit()
        messagebox.showinfo("TASK COMPLETED","USER DATA DELETED SUCCESSFULLY")
        root.destroy()

    else:
        pass

def tabulr():
    global results
    tabulr.res = []
    class Table:
        def __init__(self,root_3):
            global results
            for i in range(l):
                for j in range(3):
                    exec(f"self.e{i}_{j} = Entry(root_3,width=20,fg='blue',font=('Arial',16,'bold'))")
                    exec(f"self.e{i}_{j}.grid(row={i}+2,column={j})")
                    exec("self.e"+str(i)+"_"+str(j)+".insert(END, tabulr.res["+str(i)+"]["+str(j)+"])")
        def get(self):
            rlist = []
            for i in range(l):
                jlist = []
                tlist = []
                for j in range(3):
                    if j == 2:
                        global tpw
                        exec(f"tlist.append(self.e{i}_{j}.get())")
                        pw = tlist.pop()
                        te = Fernet(menu.uk)
                        pw = te.encrypt(pw.encode())
                        pw = str(pw).split("'")[1]
                        jlist.append(pw)
                    else:
                        exec(f"jlist.append(self.e{i}_{j}.get())")
                rlist.append(jlist)
            return rlist
    cur.execute(f"select * from user_{menu.u}")
    results=cur.fetchall()
    conn.commit()
    l = len(results)
    for i in range(l):
        tlist = []
        for j in range(3):
            if j == 2:
                pw = results[i][j]
                te = Fernet(menu.uk)
                pw = rawbytes(pw)
                pw = te.decrypt(pw)
                tlist.append(pw)
            else:
                x = results[i][j]
                tlist.append(x)
        tabulr.res.append(tlist)


    def getr():
        res = t.get()
        cur.execute(f"delete from user_{menu.u}")
        conn.commit()
        for r in res:
            u_n = r[0]
            app = r[1]
            pw = r[2]
            st = f"insert into user_{menu.u} values('{u_n}','{app}','{pw}')"
            cur.execute(st)
            conn.commit()

    root_3 = Tk()
    root_3.title("Manage Passwords")
    head_3 = Label(root_3,text= "MANAGE PASSWORDS", font=('Atial',18,'bold')).grid(row=0,column=1)
    text_3_1 = Label(root_3,text = "User Name", font=('Atial',16,'bold')).grid(row=1,column=0)
    text_3_2 = Label(root_3,text = "Application" , font=('Atial',16,'bold')).grid(row=1,column=1)
    text_3_3 = Label(root_3,text = "Pass Word" , font=('Atial',16,'bold')).grid(row=1,column=2)
    t = Table(root_3)
    b = Button(root_3,text="update",fg='blue',command=getr).grid(row=l+3,column=2)
    root_3.mainloop()

def menu(user,u_key):
    u = user
    menu.u = user
    menu.uk = u_key
    root = Tk()
    root.title('Password Manager')
    root.geometry("270x250")
    head = Label(root, text = "USER's PASSWORD MANAGER",font=('Helvetica',13,'bold')).grid(row=0)
    text_1 = Label(root, text = f"user : {u} , Select task to be performed").grid(row=1)
    button_1 = Button(root,text = "New Entry",fg = 'blue', width = 25,command = register).grid(row=2)
    button_2 = Button(root,text = "Search password",fg = 'blue', width = 25,command = search).grid(row=3)
    button_3 = Button(root,text = "Manage Passwords",fg = 'blue', width = 25,command = tabulr).grid(row=4)
    button_4 = Button(root,text = "DELETE USER",fg = 'red',width = 25,command=delete).grid(row=5)

    root.mainloop()

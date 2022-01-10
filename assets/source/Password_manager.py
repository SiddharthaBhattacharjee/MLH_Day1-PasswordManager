import subprocess
import sys
from tkinter import *
from cryptography.fernet import Fernet
import struct
try:
    import  mysql.connector as sql
except:
    subprocess.run(['pip','install','mysql-connector-python'])
    import mysql.connector as sql
from tkinter import messagebox
sys.path.insert(0,'./assets')
import tableee as tb

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

perm_key = 'dnHN8mDXO1nYKk5nZPxDZkdV75b6Wx1hhaYSQt5N5rE='
pe = Fernet(perm_key)

with open('assets/dbp.txt','r') as pwdt:
    pwd = pwdt.read()
    pwdt.close()

def register():
    def reg():
        name = entry_r1.get()
        passwd = entry_r2.get()
        pw = pe.encrypt(passwd.encode())
        pwd = str(pw).split("'")[1]
        q_key = Fernet.generate_key()
        w_key = pe.encrypt(q_key)
        u_key = str(w_key).split("'")[1]
        V_SQLInsert=f"INSERT  INTO log_id (user_id,password,key_) values ('{name}','{pwd}','"+str(u_key)+"') "
        cur.execute(V_SQLInsert)
        conn.commit()
        cur.execute(f"create table user_{name}(user_id varchar(255),application varchar(255),pw varchar(255) )")
        conn.commit()
        root_r.destroy()
    root_r = Tk()
    root_r.title('Register')
    text_r1 = Label(root_r,text = 'Register to the system',font=('Helvetica',10,'bold')).grid(row=0)
    text_r2 = Label(root_r,text = "Username : ").grid(row=1)
    text_r3 = Label(root_r,text = "Password : ").grid(row=2)
    entry_r1 = Entry(root_r,width=31)
    entry_r1.grid(row=1,column=1)
    entry_r2 = Entry(root_r,width=31)
    entry_r2.grid(row=2,column=1)
    button_r = Button(root_r,text = "Register",fg='blue',command = reg).grid(row=3,column=1)
    root_r.mainloop()

def login():
    def open_():
        name = entry_l1.get()
        passwd = entry_l2.get()

        root_l.destroy()
        V_Sql_Sel=f"select password from log_id where user_id = '{name}'"
        cur.execute(V_Sql_Sel)
        pw = cur.fetchall()
        try:
            pw = pw[0][0]
            pw = rawbytes(pw)
            pwd = pe.decrypt(pw).decode()
        except:
            pwd = ''
        if pwd != passwd:
            root_t = Tk()
            root_t.withdraw()
            messagebox.showinfo('ERROR','Invalid Username or password Please try Again')
            root_t.destroy()
            login()

        else:
            st = f"select * from log_id where user_id = '{name}'"
            cur.execute(st)
            l = cur.fetchall()
            user = l[0][0]
            q_key = l[0][2]
            w_key = rawbytes(q_key)
            u_key = pe.decrypt(w_key)
            import mainp
            mainp.menu(user,u_key)

    root_l = Tk()
    root_l.title("Login")
    text_l1 = Label(root_l,text = "Login to the System",font=('Helvetica',10,'bold')).grid(row=0)
    text_l2 = Label(root_l,text = "Username : ").grid(row=1)
    text_l3 = Label(root_l,text = 'Password : ').grid(row=2)
    entry_l1 = Entry(root_l,width=31)
    entry_l1.grid(row=1,column=1)
    entry_l2 = Entry(root_l,width=31,show='*')
    entry_l2.grid(row=2,column=1)
    button_l1 = Button(root_l,text = "  Login  ",fg='blue',command=open_).grid(row=3,column=1,sticky = E)
    text_l4 = Label(root_l,text = "Don't have an account? : ").grid(row=4,sticky=E)
    button_l2 = Button(root_l,text = 'Register',fg='blue',command=register).grid(row=4,column=1,sticky=W)
    root_l.mainloop()

def set_pass():
    global pwd
    global x
    pw_ = entry_p1.get()
    pwd = pw_
    with open('assets/dbp.txt','w') as pwdt:
        pwdt.write(pw_)
        pwdt.close()
    try:
        tb.create_database(pw_)
        pass
    except:
        pass
    root_p1.destroy()


if __name__ == "__main__":

    x=1

    while(x):
        try:
            conn=sql.connect(host='localhost',user='root',passwd=pwd,database='passwords',charset='utf8')
            cur = conn.cursor()
            x=0
        except:
            root_p1 = Tk()
            root_p1.title('Connect mySQL Database')
            head_p1 = Label(root_p1,text = "Failed to connect to Database , ",font=('Helvetica',10,'bold'))
            head_p2 = Label(root_p1,text = "Please Enter your mySQL password",font=('Helvetica',10,'bold'))
            head_p1.grid(row=0)
            head_p2.grid(row=0,column=1)
            text_p1 = Label(root_p1,text = "mySQL Password : ")
            entry_p1 = Entry(root_p1,width=31,bd=4,relief=RIDGE)
            button_p1 = Button(root_p1,text ='Continue',fg='blue',command=set_pass)
            text_p1.grid(row=1,sticky=E)
            entry_p1.grid(row=1,column=1,sticky=W)
            button_p1.grid(row=2,column=2,sticky=W)
            root_p1.mainloop()

    login()

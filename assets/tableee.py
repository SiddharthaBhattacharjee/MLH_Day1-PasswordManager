import mysql.connector as sql

def create_database(password):

    pw = password

    conn=sql.connect(host='localhost',user='root',password=pw,charset='utf8')
    mycursor=conn.cursor()
    conn.autocommit = True
    mycursor.execute("create database passwords")
    mycursor.execute("use passwords")
    mycursor.execute("create table log_id(user_id varchar(20) primary key ,password  varchar(255), key_ varchar(255))")

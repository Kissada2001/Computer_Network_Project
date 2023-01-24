import socket
import time
import os
import sys
import sqlite3
from datetime import datetime

print('\n\n','*'*10 + ' >> Payment Record << ' + '*'*10,'\n\n')
TCP_IP = "127.0.0.1"
TCP_PORT = 5678
BUFFER_SIZE = 1024

username = "" #รอรับค่าชื่อผู้ใช้จากผู้ใช้
password = "" #รอรับรหัสผ่านจากผู้ใช้

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))

flag_login = 0

def Clear():
    os.system('cls')

def Main(): #เมนู
    print('>>>> 1 .Login' + '\n'
          '>>>> 2. Register \n\n')
    while True:
        Input = int(input('>> Please select a menu (number): '))
        Clear()
        if Input == 1:
            Login()
            break
        elif Input == 2:
            Register()
            time.sleep(2)
            Login()
            break
        else:
            print('>> Please enter the correct number.!')
    global flag_login
    if flag_login == 1:
        menu()

    s.close()
    print('='*10 + '  EXIT  ' + '='*10)

def Login(): #ระบบล็อกอิน
    while True:
        print("\n >>>>:::: Login ::::<<<<")     
        s.send(bytes("--LOGIN--","utf-8"))
        global username
        global password
        username = input("Please enter username: ")
        s.send(bytes(username,"utf-8"))
        password = input("Please enter your password: ")
        Clear()
        s.send(bytes(password,"utf-8"))
        s.send("break".encode("utf-8"))

        while 1:
            data = s.recv(BUFFER_SIZE).decode("utf-8")
            if not data: break
            elif data == "yes":
                #login สำเร็จ
                print("\n  ===== Login successfully ====\n")
                print("  Hello, ",username)
                global flag_login
                flag_login = 1
                break
            elif data == "no":
                #login ไม่สำเร็จ
                print("You failed to login.")
                print("Please try again.\n")
                break
        if flag_login == 1:
            break

def Register():
    print("\n >>>>:::: Register ::::<<<<")   
    global username
    global password
    while True:
        username = input("Please enter username: ")
        password = input("Please enter your password: ")
        password_con = input("Please enter your password again for confirmation: ")
        if password == password_con:
            s.send(bytes("--REG--","utf-8"))
            time.sleep(0.1)
            s.send(bytes(username,"utf-8"))
            time.sleep(0.1)
            s.send(bytes(password,"utf-8"))
            time.sleep(0.1)
            s.send("break".encode("utf-8"))
            print("A request has been sent to the server.")
            break
        else:
            print("Please make sure your password and confirmation password match.")
    #ทำการส่งข้อมูลไปสมัคร
    while 1:
        data = s.recv(BUFFER_SIZE).decode("utf-8")
        if not data: break
        elif data == "yes":
            #login สำเร็จ
            print("Successful registration.\n")
            time.sleep(0.1)
            Clear()
            break

def menu():
    
    if username != "admin" :
        while True:
            print("\n >>>>:Main Menu:<<<<\n")
            print("-----> 1. Add Data ")
            print("-----> 2. View recording history")
            print("-----> 3. EXIT")
            Input = int(input('>> Please select a menu (number): '))
            Clear()
            if Input == 1:
                AddData()
            if Input == 2:
                History()
            if Input == 3:
                Exit()
    else: 
        while True:
            admin()   


    
def admin_history():
    f = open('admin_data.txt', 'r',encoding='utf-8')
    data = f.read()
    print(data)
    

def admin_User():
    conn_db = sqlite3.connect('customers.db')
    c=conn_db.cursor()
    print("====== Show User ======")
    c.execute("SELECT * FROM customer")
    for no in c.fetchall():
        print("Username & Password",no)
    conn_db.commit()
    conn_db.close()
   

def admin():
    print("\n\n\n>>>>:Main Menu (ADMIN):<<<< :\n")
    print("-----> 1. View recording history")
    print("-----> 2. View a list of all service recipients.")
    print("-----> 3. EXIT")
    Input1 = int(input('>> Please select a menu (number): '))
    Clear()
    if Input1 == 1:
        admin_history()
    if Input1 == 2:
        admin_User()
    if Input1 == 3:
        Exit()

def AddData():
    while True:
        f = []
        f = open('data.txt','a+',encoding='utf-8')
        f2 = open('admin_data.txt' ,'a+',encoding='utf-8')
        print('====== Add Data ====== ')
        name = input('->> Enter Data Name : ')
        cdtn = input('->> Enter Creditor Name : ')
        amout = input('->> Enter Total Amount Owed : ')
        mobile = input('->> Enter Creditor Mobile Number : ')
        Date = input('->> Enter Due Date : ')
        Datetime = str(datetime.now())
        print("\n")
        print(username)
        print(" Data Name: %s\n Creditor Name: %s\n Total Amount Owed: %s\n Creditor Mobile Number: %s\n Due Date: %s\n" %(name, cdtn, amout, mobile, Date))
        print(" Date time recording : %s\n" %Datetime)
        f.write(username)
        f.write("\n->> Data Name: %s\n->> Creditor Name: %s\n->> Total Amount Owed: %s\n->> Creditor Mobile Number: %s\n->> Due Date: %s\n" %(name, cdtn, amout, mobile, Date))
        f.write("->> Datetime recording : %s\n\n" %Datetime)
        f2.write(username)
        f2.write("\n->> Data Name: %s\n->> Creditor Name: %s\n->> Total Amount Owed: %s\n->> Creditor Mobile Number: %s\n->> Due Date: %s\n" %(name, cdtn, amout, mobile, Date))
        f2.write("->> Datetime recording : %s\n\n" %Datetime)
        f.close()
        f2.close()
        title = input('Continue Y , Exit: N : ')
        if title =='N':
            menu()
        
def History():
    
    places = []
    with open('data.txt', 'r',encoding='utf-8') as filehandle:
        for line in filehandle:
            currentPlace = line[:-1]
            places.append(currentPlace)
    #ปริ้น 
    k=0
    while k < len(places):
        if(places[k] == username):
            print(places[k+1])
            print(places[k+2])
            print(places[k+3])
            print(places[k+4])
            print(places[k+5])
            print(places[k+6],"\n")
            
        k=k+1
    
def Exit():
    s.send("--QUIT--".encode("utf-8"))
    print("!!!!!!!!!!!!!!!>>>THANK YOU<<<!!!!!!!!!!!!!!!! ^_^")
    sys.exit()


Main() #รันโปรแกรม

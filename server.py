import socket
import time
import traceback
import sqlite3
from threading import Thread


print('\n\n','='*10 + '  SERVER  ' + '='*10,'\n\n')
TCP_IP = "127.0.0.1"
TCP_PORT = 5678
BUFFER_SIZE = 1024

def Login(connection ,ip):
    member_profile = []
    print(connection,"Have been connected to request login")
    while True:
        data = connection.recv(BUFFER_SIZE).decode("utf-8")
        if not data: break
        if len(member_profile) > 2 or len(member_profile) == 2:
            break
        member_profile.append(data)
    print("Username & Password: ",member_profile)

    #check id
    conn_db = sqlite3.connect('customers.db')
    c=conn_db.cursor()
    c.execute("SELECT * FROM customer")
    flag = 1
    for no in c.fetchall():
        if no == tuple(member_profile):
            flag = 0
            break
    if flag == 0:
        connection.send("yes".encode("utf-8"))
    else:
        connection.send("no".encode("utf-8"))
    conn_db.commit()
    conn_db.close()
    
    print("Login successfully")

def Register(connection ,ip):
    member_profile = []
    while True:
        data = connection.recv(BUFFER_SIZE).decode("utf-8")
        if not data: break
        elif len(member_profile) > 2 or len(member_profile) == 2:
            break
        print("rev: ",data)
        member_profile.append(data)
        print(member_profile)
        print(len(member_profile))
    print("Username & Password: ",member_profile)

   #check id
    conn_db = sqlite3.connect('customers.db')
    c=conn_db.cursor()
    sqlite_insert_with_param = """INSERT INTO customer
                          (Username, Password) 
                          VALUES (?, ?);"""
    data_tuple = (member_profile[0],member_profile[1])
    c.execute(sqlite_insert_with_param, data_tuple)
    time.sleep(0.1)
    print("Saved to the database successfully.")
    conn_db.commit()
    conn_db.close()
    connection.send("yes".encode("utf-8"))
    print("Registered successfully")



def process_input(input_str):
    print("Processing the input received from client")

    return str(input_str).upper()

def receive_input(connection):
    client_input = connection.recv(BUFFER_SIZE)
    
    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input)

    return result

def client_thread(connection, ip, port):
    is_active = True

    while is_active:
        client_input = receive_input(connection)

        if "--LOGIN--" in client_input:
            print("Members are currently logged in....")
            Login(connection, ip)
        elif "--REG--" in client_input:
            print("Members request to register to login...")
            Register(connection, ip)
        elif "--QUIT--" in client_input:
            print("Client has made a request to log out")
            connection.close()
            print("Connection " + ip + ":" + port + " has logged out")
            is_active = False
        else:
            print("Processed result: {}".format(client_input))
            connection.sendall("-".encode("utf8"))
            

def Main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP,TCP_PORT)) #เชื่อมต่อ
    s.listen(5)
    print("The server has been running.")

    #flag_server = 0
    while True:
        conn,addr = s.accept()
        ip,port = str(addr[0]), str(addr[1])
        print("There is a connection...")
        try:
            Thread(target=client_thread,args=(conn,ip,port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
    s.close()
    
Main()
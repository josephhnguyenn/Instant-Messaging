import socket
import threading
import time
from datetime import datetime
import thread

all_connections = []
all_address = []
all_names = []
def disconnect(conn,addr,name):
    all_connections.remove(conn)
    all_address.remove(addr)
    all_names.remove(name)
    for x in range(len(all_connections)):
        all_connections[x].send(name.encode() + b" has left the chat\n")

def activeUserList():
    print(all_connections)
    print(all_address)
    print(all_names)

def newclient(conn, addr):
    #The first data received will ALWAYS be the screen name of the user
    name = conn.recv(1024)
    name = name.decode()
    print (name + ' has connected.\n')
    for x in range(len(all_connections)-1):
        all_connections[x].send(name.encode() + b" has entered the chat.")
    all_names.append(name)
    while True:	
        data = conn.recv(1024)
        data = data.decode()
        if(data=="$$$$DISCONNECT$$$$"):
            disconnect(conn,addr,name)
            activeUserList()
        elif(data=="$$$$UPDATE$$$$"):
            msg = ""
            for x in range(len(all_connections)):
                if (x == len(all_connections)-1):
                    msg = msg + all_names[x]
                else:
                    msg = msg + all_names[x] + "\n"    
            conn.send(b"$$$$UPDATING$$$$")
            time.sleep(0.5)
            print(msg)
            conn.send(msg.encode())
        elif(data):	
            print (name + ">> " + data)
            ts = datetime.now()
            ts = ts.strftime("(%H:%M)")
            data = "[" + ts + "] " + name  + ">> " + data
            for x in range(len(all_connections)):
                all_connections[x].send(data.encode())
              
	

IP = '192.168.1.152'
PORT = 5006

DATA_SIZE = 1024 
s = socket.socket()
s.bind((IP, PORT))
s.listen(5)

while True: 
    conn, addr = s.accept()
    all_address.append(addr)
    all_connections.append(conn)
    thread.start_new_thread(newclient,(conn,addr))

s.close()


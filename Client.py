from Tkinter import *
from threading import Thread
from time import sleep
import socket
import time
from datetime import datetime

IP = "127.0.0.1"
PORT = 5031
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Delivered = ""
sock.connect((IP,PORT))
username = ""

#THIS IS SENDING CLIENT (RETIRED)
class send(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        msg = usernameBox2.get()
        Delivered = ">> " + msg
        sock.send(msg.encode())

#THIS IS RECEIVING CLIENT	
class receive(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
	global username
        while True:
            data = sock.recv(1024)
            #data = data.decode()
            if(data==Delivered):
                print("Delivered")
	    elif(data == "$$$$UPDATING$$$$"):
		userList.delete("1.0",END)
		active = sock.recv(1024)
		userList.insert(INSERT,active) 
            else:
                print(data)
		chatArea.insert(INSERT,data + "\n")
class xupdate(Thread):
    def __init__(self):
        Thread.__init__(self)
	self.daemon = True
	self.start()
    def run(self):
	while True:
      	    x = 1

def disconnect(event): #MAP THIS TO DISCONNECT BUTTON
    sock.send("$$$$DISCONNECT$$$$")
    chatArea.insert(INSERT, "You have left the chat\n")
    sock.close()    

def update(event):
    sock.send("$$$$UPDATE$$$$")
 #   data = sock.recv(1024)
 #   userList.insert(INSERT,data)

def retrieve(event):
    global username
    username = usernameBox.get()
#    sock.connect((IP,PORT))
    sock.send(username.encode())
    print("Connected to server.")
    createWidgets2()
        
def createWidgets2():       #Sets values for all the widgets init. making them apear in the GUI
    usernameBox.destroy()

    textArea.pack(side=BOTTOM)
    
    usernameBox2.pack(side=LEFT, padx=10)
    
    sendButton.pack(side=RIGHT, padx=10)
    
    usernameLabel.destroy()
    
    groupChat.pack(side = LEFT)
    
    activeUsers.pack(side = LEFT)
    
    chatArea.pack(side = TOP, padx=10)
    
    userList.pack(side=BOTTOM)
    
    activeUsersLabel.pack(side=TOP)
    
    updateButton.pack(side=BOTTOM, pady = 10)
    
    userList.pack(side=BOTTOM)
    
    activeUsersLabel.pack(side=BOTTOM, pady =10)
    
    discButton.pack(side= TOP)

receive()    

def retrieve2(event):
    msg = usernameBox2.get()
    sock.send(msg)
#    sendMessage = send()
#    sendMessage.__init__()
#    sendMessage.run()
#    receiveMessage = receive()
#    receiveMessage.__init__()
#    receiveMessage.run()
    usernameBox2.delete("0",last=END)
        

##################### Part Zero #######################

root = Tk()               #Creation of main panel
root.geometry("800x480")
groupChat = Frame(root)   #Left pane for group chat use
groupChat.pack()
activeUsers = Frame(root) #Right Pane for user list

##################### Part One  #######################

usernameBox = Entry(groupChat, bd=5) #Input username textbox
usernameBox.pack(side = RIGHT)
usernameLabel =  Label(groupChat, text="User Name") #Label for username
usernameLabel.pack(side=LEFT)

usernameBox.bind("<Return>",retrieve) #Bind input to Enter key

##################### Part Two  #######################
chatArea = Text(groupChat)      #Text area to display chat messages (Left Pane)

userList = Text(activeUsers, height =15) #List Box to recieve online users (Right Pane)

var = StringVar()               #Label for listbox above(Right Pane)
activeUsersLabel = Label(activeUsers, textvariable=var)
var.set("Online Users")

textArea = Frame(groupChat)     #Sub left pane to organized send button and message entry

usernameBox2 = Entry(textArea, bd=5)    #Area to put in text to send
usernameBox2.bind("<Return>",retrieve2) #Bind Enter key to retrieve2 function to send message and clear box

sendButton = Button(textArea, text ="Send") #Creation of send button

discButton = Button(activeUsers, text ="Disconnect") #Creation of disconnect button
discButton.bind("<ButtonRelease>", disconnect )

updateButton= Button(activeUsers, text ="Update List") #Creation of send button
updateButton.bind("<ButtonRelease>", update)

root.mainloop()
root.destroy()

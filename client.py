import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from tkinter import *

firstclick = True
m_c = True
name_set =False
#----Socket code----
print("(Press enter for default settings)")
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 5431
else:
    PORT = int(PORT)
if not HOST:
    HOST = "localhost"

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket.socket(AF_INET, SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(ADDR)


def on_entry_click(event):
    """function that gets called whenever entry1 is clicked"""        
    global firstclick

    if firstclick: # if this is the first time they clicked it
        firstclick = False
        entry_field.delete(0, "end") # delete all the text in the entry

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")
    #if msg.capitalize() == "Bye":
     #   on_closing(True)
          # Clears input field.
    #else:
    client_socket.send(bytes(msg, "utf8"))
    

def on_closing(event=None):
    try:
        client_socket.send(bytes("{quit}", "utf8"))
        client_socket.close()
        msg_list.insert(END, "You have left the chat room!")
    except:
        print("error")
        
    root.quit()


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(END, msg)
        except OSError:  # Possibly client has left the chat.
            break
def hide_name(event):
    print("HEllo")


def caps(event):
    msg = my_msg.get()
    global m_c
    if m_c:
        my_msg.set(msg.capitalize())
    if msg:
        m_c = False
    else:
        m_c =True

def logout():
    try:
        client_socket.send(bytes("{quit}", "utf8"))
        client_socket.close()
        msg_list.insert(END, "You have left the chat room!")
        
    except:
        print("error")

    

root = Tk()
root.title("Chat Room")

messages_frame = Frame(root)
my_msg2 = StringVar() 
my_msg2.set("Enter you name") 
my_msg = StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
ll = StringVar() 
ll= "Logout"

entry_field = Entry(root, textvariable=my_msg, width = 75 )
send_button = Button(root, text="Send", command=send ,width = 7)
send_button.config(state='disabled')

send_button2 = Button(root, text=ll, command=logout ,width = 7)
send_button2.config(state='disabled')

name_set = False
name_entry = Entry(root, textvariable=my_msg2,width = 50,justify = CENTER)
name_entry.bind('<FocusIn>',lambda a : name_entry.delete(0, "end"))

name_entry.bind("<Return>",lambda a :( name_entry.config(state='disabled'),
    send_button.config(state='normal'),
    send_button2.config(state='normal'),
    entry_field.config(state='normal'),
    client_socket.send(bytes((my_msg2.get()).capitalize(), "utf8")),
    my_msg2.set("Welcome to the chat room "+my_msg2.get())))
name_entry.pack(side=TOP ,pady = 5)



scrollbar = Scrollbar(messages_frame,width = 20)  # To navigate through past messages.
# Following will contain the messages.
msg_list = Listbox(messages_frame, height=15, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=BOTH)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()

entry_field.bind('<FocusIn>',on_entry_click)
entry_field.bind("<Return>",send)
entry_field.bind("<Key>",caps)
entry_field.config(state='disabled')

entry_field.pack(side=LEFT, padx =10)
send_button2.pack(side=RIGHT, padx =10 ,pady = 5 )
send_button.pack(side=RIGHT ,padx =10 ,pady = 5 )


root.protocol("WM_DELETE_WINDOW", on_closing)



receive_thread = Thread(target=receive)
receive_thread.start()
root.mainloop()









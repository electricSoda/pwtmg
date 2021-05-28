from tkinter import *
from tkinter import font
from tkinter import simpledialog
from tkinter import messagebox
import sys
import cmd
import pwtmg
import socket
import threading
import time

#local tcp variables
port = 3000
ip = "161.97.198.58"
address = (ip, port)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = "/disconnect"

def rient():
    global client, pyclient
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(address)
    except Exception as e:
        messagebox.showinfo("Error", "Could not connect to main server, this probably means that the server is down. Please try again later.")

    pyclient = pwtmg.client(port, ip, address, HEADER, FORMAT, DISCONNECT_MSG, client)
    pyclient.sendmsg("%%%%%" + name)

def startReceiving():
    global c
    while True:
        try:
            receiving = pyclient.receive()
            if receiving:
                c.printLine(str(receiving))
        except Exception as e:
            messagebox.showinfo("Error",
                                "Could not connect to main server, this probably means that the server is down. Please try again later.")
            root.destroy()
            sys.exit()



def startClient():
    global thread, thread2

    thread = threading.Thread(target=rient)  # create a thread on cpu to run startClient() simultaneously
    thread.start()

    time.sleep(0.5)

    thread2 = threading.Thread(target=startReceiving)
    thread2.start()

#setup
root = Tk()
root.title('PWTMG')
root.geometry("700x500")
root.iconbitmap('favicon.ico')
root.config(bg='black')

#ask for name
name = simpledialog.askstring("Username", "Please enter a name:",parent=root)

#commandline
prompt = Listbox(root)
prompt.config(bg='black', fg='white', font=font.Font(family = 'Lucida Console', size=13))
prompt.pack(fill=BOTH, expand=True)

#command input
pinput = StringVar()

def validate(new_value):
    return new_value.startswith("> ")

vcmd = root.register(validate)

def command(event):
    text = pinput.get()
    pin.delete(2, END)
    if text == '> exit' or text=='> /disconnect':
        pyclient.sendmsg(DISCONNECT_MSG)
        root.destroy()
        exit()
    elif text.startswith("> /"):
        c.checkCommand(text[3:])
        c.printLine(text)
    else:
        newtext = name + " " + text
        sended = pyclient.sendmsg(newtext)

pin = Entry(root)
pin.config(background = 'black', foreground = 'white', validate="key", validatecommand=(vcmd, "%P"), textvariable = pinput, font = font.Font(family = 'Lucida Console', size = 15))
pin.config(insertbackground = 'white', insertofftime = 0, insertontime = 0, insertwidth = 2)
pin.focus_set()
pin.bind('<Return>', command)
pin.insert(0, '> ')
pin.pack(fill=X)

c = cmd.commandLine(root, prompt)

#startup
c.printLine("Python Word Text Multiplayer Game")
c.printLine("(c) Justin Ge. All rights reserved.")
c.printLine(" ")

#window on close
def on_closing():
    pyclient.sendmsg(DISCONNECT_MSG)
    root.destroy()
    exit()

root.protocol("WM_DELETE_WINDOW", on_closing)

#mainloop and client
root.after(0, startClient)
root.mainloop()
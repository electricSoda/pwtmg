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
import sqlite3

#local tcp variables
port = 3000
ip = "161.97.198.58"
address = (ip, port)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = "/disconnect"

#some variables
pinged = False

def rient():
    global client, pyclient
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(address)
    except Exception as e:
        messagebox.showinfo("Error", "Could not connect to main server, this probably means that the server is down. Please try again later.")

    pyclient = pwtmg.client(port, ip, address, HEADER, FORMAT, DISCONNECT_MSG, client)
    pyclient.sendmsg("%%%%%" + username)

def startReceiving():
    global c, pinged
    while True:
        try:
            receiving = pyclient.receive()
            if receiving:
                if receiving == "*****PONG":
                    pinged = True
                else:
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

username = None

#ask for name
def startLogin():

    # databases
    usersdb = sqlite3.connect('users.db')
    c = usersdb.cursor()

    # c.execute("""CREATE TABLE users (
    #             username text,
    #             password text
    #             )""")

    # tkinter
    win = Tk()
    win.iconbitmap('favicon.ico')
    win.title('Login')
    win.geometry("300x300")

    usernameL = Label(win, text='Username:')
    usernameL.pack(pady=10)

    usernameE = Entry(win)
    usernameE.pack()

    passwordL = Label(win, text='Password:')
    passwordL.pack(pady=10)

    passwordE = Entry(win, show="*")
    passwordE.pack()

    def check():
        submit.config(text='Processing...', state=DISABLED)
        get1 = usernameE.get()
        get2 = passwordE.get()

        if get1 == '' or get2 == '' or get1 == ' ' or get2 == ' ':
            status.config(text='Invalid credentials, please try again!', fg='red')
            submit.config(text='Submit', state=NORMAL)
        else:
            c.execute(f"SELECT * FROM users WHERE username='{get1}'")
            account = c.fetchone()
            if not account:
                status.config(text='Invalid username, please try again!', fg='red')
                submit.config(text='Submit', state=NORMAL)
            else:
                if get2 == account[1]:
                    status.config(text='Success!', fg='green')
                    submit.config(text='Submit', state=NORMAL)
                    win.destroy()
                    global username
                    username = account[0]
                    # mainloop and client
                    root.after(5, startClient)
                    root.deiconify()
                    c.close()
                else:
                    status.config(text='Invalid password, please try again!', fg='red')
                    submit.config(text='Submit', state=NORMAL)

    submit = Button(win, text='Submit', bg='white', relief=RAISED, command=check)
    submit.pack(pady=10)

    def signup():
        for widget in win.winfo_children():
            widget.destroy()

        usernameL = Label(win, text='New Username:')
        usernameL.pack(pady=10)

        usernameE = Entry(win)
        usernameE.pack()

        passwordL = Label(win, text='New Password:')
        passwordL.pack(pady=10)

        passwordE = Entry(win, show="*")
        passwordE.pack()

        password2L = Label(win, text='Type Your New Password Again:')
        password2L.pack(pady=10)

        password2E = Entry(win, show='*')
        password2E.pack()

        # another bad practice, having functions inside
        # functions. But i'm too lazy ;)
        def check():
            get1 = usernameE.get()
            get2 = passwordE.get()
            get3 = password2E.get()

            if get2 == get3:
                if get1 == '' or get2 == '' or get3 == '' or get1 == ' ' or get2 == ' ' or get3 == ' ':
                    submit.config(text='Sign Up', state=NORMAL)
                    status.config(text='Invalid credentials, please try again!', fg='red')
                    status.pack(pady=10)
                else:
                    submit.config(text="Processing...", state=DISABLED)
                    status.config(text='')
                    status.pack_forget()

                    c.execute(f"SELECT * FROM users WHERE username='{get1}'")
                    account = c.fetchone()

                    if account:
                        submit.config(text='Sign Up', state = NORMAL)
                        status.config(text='User already exists.')
                        status.pack()
                    else:
                        c.execute(f"INSERT INTO users VALUES ('{get1}', '{get2}')")

                        usersdb.commit()
                        usersdb.close()
                        win.destroy()
                        startLogin()
                        global username
                        username = get1
            else:
                status.config(text='Your passwords do not match.')
                status.pack(pady=10)

        submit = Button(win, text="Sign Up", bg='white', relief=RAISED, command=check)
        submit.pack(pady=10)

        status = Label(win)
        status.config(fg='red')

        lab = Label(win, text="Don't forget your credentials to your accound!")
        lab.pack()

    noacc = Button(win, text='Sign Up', bg='white', relief=RAISED, command=signup)
    noacc.pack(pady=10)

    status = Label(win)
    status.pack()

    win.mainloop()

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
        if text == "> /ping":
            pyclient.sendmsg("*****PING")
            begin = time.time() #start milliseconds before message is received
            while not pinged:
                pass
            end = time.time()
            elapsedtime = end - begin
            elapsedtime = elapsedtime * 100
            elapsedtime = round(elapsedtime, 1)
            c.printLine("> Pong! Your ping is: " + str(elapsedtime) + " ms")
            return

        c.checkCommand(text[3:])
        c.printLine(text)
    else:
        newtext = username + " " + text
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

root.withdraw()
root.after(0, startLogin)
root.mainloop()
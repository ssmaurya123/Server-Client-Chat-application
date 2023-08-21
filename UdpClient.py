from tkinter import *
import _thread
import socket

def initialize_client():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = 'localhost'
    port = 12345
    s.bind((host, port))

def update_chat(msg, state):
    global chatlog
    chatlog.config(state=NORMAL)
    if state==0:
        chatlog.insert(END, 'YOU : ' + msg)
    else:
        chatlog.insert(END, 'OTHER : ' + msg)
    chatlog.config(state=DISABLED)
    chatlog.yview(END)

def send():
    global textbox
    msg = textbox.get("0.0", END)
    update_chat(msg, 0)
    s.sendto(msg.encode('ascii'), ('localhost', 1234))
    if msg.strip() == "exit":
        s.close()
        import sys
        sys.exit(0)
    textbox.delete("0.0", END)

def receive():
    while True:
        try:
            data = s.recvfrom(1024)[0]
            msg = data.decode('ascii')
            if msg != "":
                update_chat(msg, 1)
        except:
            pass

def press(event):
    send()

def GUI():
    global chatlog
    global textbox
    gui = Tk()
    gui.title("Client Chat")
    gui.geometry("380x430")
    chatlog = Text(gui, bg='cyan')
    chatlog.config(state=DISABLED)
    sendbutton = Button(gui, bg='lime', fg='purple', text='SEND', command=send)
    textbox = Text(gui, bg='white')
    chatlog.place(x=6, y=6, height=386, width=370)
    textbox.place(x=6, y=401, height=20, width=265)
    sendbutton.place(x=300, y=401, height=20, width=50)
    textbox.bind("<KeyRelease-Return>", press)
    _thread.start_new_thread(receive, ())
    gui.mainloop()

if __name__ == '__main__':
    chatlog = textbox = None
    initialize_client()
    GUI()

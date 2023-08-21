from tkinter import *
from socket import *
import _thread


def initialize_client():
    s = socket(AF_INET, SOCK_STREAM)
    host = 'localhost'
    port = 1234
    s.connect((host, port))
    return s


def update_chat(msg, state):
    global chatlog
    chatlog.config(state=NORMAL)
    if state == 0:
        chatlog.insert(END, 'YOU: ' + msg)
    else:
        chatlog.insert(END, 'OTHER: ' + msg)
    chatlog.config(state=DISABLED)
    chatlog.yview(END)


def send():
    global textbox
    msg = textbox.get("0.0", END)
    update_chat(msg, 0)
    s.send(msg.encode('ascii'))
    textbox.delete("0.0", END)


def receive():
    while 1:
        try:
            data = s.recv(1024)
            msg = data.decode('ascii')
            if msg != "":
                update_chat(msg, 1)
        except:
            pass


def press(event):
    send()


# GUI function
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
    s = initialize_client()
    GUI()

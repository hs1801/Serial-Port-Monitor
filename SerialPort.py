import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import serial


# *********************** SEND DATA ***********************

def send_char(event):
    char = event.char
    if char == '\r':
        char = '\r\n'
    char = char.encode('utf-8')

    ser.write(char)


def startsending():
    txt1.config(state="normal")
    txt1.bind("<KeyPress>", send_char)


def stopsending():
    txt1.config(state="disabled")
    txt1.unbind("<KeyPress>")


# *********************** RECEIVE DATA ***********************

def receive_char():
    while receiving.get():
        char = ser.read().decode('utf-8')
        if char:
            txt2.insert('end', char)


def startreceiving():
    receiving.set(True)
    txt2.config(state="normal")
    thread1 = Thread(target=receive_char)
    thread1.start()


def stopreceiving():
    receiving.set(False)
    txt2.config(state="disabled")


# *********************** CONNECTION ***********************

def connect():
    global ser
    try:
        ser = serial.Serial(port=port.get(), stopbits=int(stop.get()),
                            baudrate=baud.get(), bytesize=int(size.get()),
                            parity=par.get()[0], timeout=1,
                            xonxoff=[True if flow.get() ==
                                     'Hardware' else False][0],
                            dsrdtr=[True if flow.get() ==
                                    'Software' else False][0],
                            rtscts=[True if flow.get() == 'Software' else False][0])

        ser.close()
        ser.open()

        messagebox.showinfo("Serial Port Communication",
                            "Connected Successfully")
        startsending()
        startreceiving()

        butcon.grid_forget()
        butdis.grid(row=5, column=1, pady=5)

        port.config(state='disabled')
        baud.config(state='disabled')
        size.config(state='disabled')
        stop.config(state='disabled')
        flow.config(state='disabled')

    except Exception as error:
        messagebox.showinfo("Serial Port Communication", f'{error}')


def disconnect():
    stopsending()
    stopreceiving()
    ser.close()
    butdis.grid_forget()
    butcon.grid(row=5, column=1, pady=5)

    port.config(state='normal')
    baud.config(state='normal')
    size.config(state='normal')
    stop.config(state='normal')
    flow.config(state='normal')


def clear():
    txt1.delete('1.0', 'end')
    txt2.delete('1.0', 'end')


def close():
    if butdis.grid_info():
        disconnect()
    yesno = messagebox.askquestion(
        'Serial Port Communication', 'Are you sure to close the application?')
    if yesno == 'yes':
        win.destroy()


# *********************** MAIN ***********************

win = tk.Tk()
win.title("Serial Port Communication")
win.resizable(0, 0)
win.protocol("WM_DELETE_WINDOW", close)

tk.Label(text="RS232 - SERIAL PORT COMMUNICATION",
         font=('Arial', 20, 'bold')).grid(row=0, column=0,
                                          padx=20, pady=20, columnspan=2)

# SENDER FRAME
fsend = tk.Frame(win)
fsend.grid(row=1, column=0, padx=20)

tk.Label(fsend, text="Send Data:", font=('Arial', 10)).grid(
    row=0, column=0, sticky='w')
txt1 = tk.Text(fsend, height=15, width=90,
               state="disabled", font=('Arial', 10))
txt1.grid(row=1, column=0)

# RECEIVER FRAME
receiving = tk.BooleanVar()
receiving.set(False)

freceive = tk.Frame(win)
freceive.grid(row=2, column=0, padx=20)

tk.Label(freceive, text="Received Data:", font=('Arial', 10)).grid(
    row=2, column=0, sticky='w')
txt2 = tk.Text(freceive, height=15, width=90,
               state="disabled", font=('Arial', 10))
txt2.grid(row=3, column=0)


# SETTINGS FRAME
frame1 = tk.Frame(win)
frame1.grid(row=1, column=1, rowspan=2, padx=20)

tk.Label(frame1, text="Port: ", font=('Arial', 10)).grid(
    row=0, column=0, sticky='w')

portlist = ["COM"+str(i) for i in range(1, 101)]

baudlist = [600, 1200, 2400, 4800, 9600,
            14400, 19200, 38400, 56000, 57600, 115200]

port = ttk.Combobox(frame1, values=portlist, font=('Arial', 10))
port.grid(row=0, column=1, sticky='w', pady=10)
port.set(portlist[2])

tk.Label(frame1, text="Baud Rate: ", font=('Arial', 10)).grid(
    row=1, column=0, sticky='w')

baud = ttk.Combobox(frame1, values=baudlist, font=('Arial', 10))
baud.grid(row=1, column=1, sticky='w', pady=10)
baud.set(baudlist[4])

tk.Label(frame1, text="Data Size: ", font=('Arial', 10)).grid(
    row=2, column=0, sticky='w')

size = ttk.Combobox(frame1, values=['7', '8'], font=('Arial', 10))
size.grid(row=2, column=1, sticky='w', pady=10)
size.set('8')

tk.Label(frame1, text="Parity: ", font=('Arial', 10)).grid(
    row=3, column=0, sticky='w')

par = ttk.Combobox(frame1, values=['None', 'Odd', 'Even'], font=('Arial', 10))
par.grid(row=3, column=1, sticky='w', pady=10)
par.set('None')

tk.Label(frame1, text="Stop Bit: ", font=('Arial', 10)).grid(
    row=3, column=0, sticky='w')

stop = ttk.Combobox(frame1, values=['1', '2'], font=('Arial', 10))
stop.grid(row=3, column=1, sticky='w', pady=10)
stop.set('1')

tk.Label(frame1, text="Flow Control: ", font=('Arial', 10)).grid(
    row=4, column=0, sticky='w')

flow = ttk.Combobox(
    frame1, values=['Hardware', 'Software', 'None'], font=('Arial', 10))
flow.grid(row=4, column=1, sticky='w', pady=10)
flow.set('None')

butcon = tk.Button(frame1, text="CONNECT", command=connect,
                   width=15, font=('Arial', 10))
butcon.grid(row=5, column=1, pady=5)

butdis = tk.Button(frame1, text="DISCONNECT",
                   command=disconnect, width=15, font=('Arial', 10))

butclr = tk.Button(frame1, text="CLEAR",
                   command=clear, width=15, font=('Arial', 10))
butclr.grid(row=7, column=1, pady=5)

butexit = tk.Button(frame1, text="EXIT", command=close,
                    width=15, font=('Arial', 10))
butexit.grid(row=8, column=1, pady=5)

# CREDITS
tk.Label(text="Developed by Harshit Singhal", font=('Arial', 10)).grid(
    row=3, column=1, sticky='e', padx=20)

win.mainloop()

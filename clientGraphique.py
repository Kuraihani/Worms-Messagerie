import tkinter as tk
from tkinter import *
from client import Client
from tkinter import scrolledtext
import json
import datetime

class ClientApp(tk.Tk):    
    def __init__(self, *args, **kwargs):          
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Messagerie")
        self.mainContainer()   
        self.showFrame(StartPage)

    def mainContainer(self):
        container = tk.Frame()  
        container.pack(expand=YES)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}  
        for F in (StartPage, PageMain):  
            frame = F(container, self)
            frame.configure(bg='dodgerblue')
            self.frames[F] = frame 
            frame.grid(row = 0, column = 0, sticky ="nsew")

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
    def passDataDialog(self, text):
        self.frames[self.pages[1]].get_text(text)



class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = Label(self, text="Messagerie", font=("Courrier", 35), bg='dodgerblue',
                            fg='white')
        label_title.pack(pady=(80,0))

        label_username = Label(self, text="Pseudo", font=("Courrier", 25), bg='dodgerblue', fg='white')
        label_username.pack()

        self.username_entry = Entry(self, font=("Helvetica", 20))
        self.username_entry.pack()

        label_server = Label(self, text="Serveur", font=("Courrier", 25), bg='dodgerblue', fg='white')
        label_server.pack()

        self.server_entry = Entry(self, font=("Helvetica", 20))
        self.server_entry.pack()
    
        label_port = Label(self, text="Port", font=("Courrier", 25), bg='dodgerblue', fg='white')
        label_port.pack()

        self.port_entry = Entry(self, font=("Helvetica", 20))
        self.port_entry.pack()

        validate_button = Button(self, text="Valider", font=("Courrier", 25), bg='white', fg='dodgerblue', 
            command=lambda: self.validateConfig({'username': self.username_entry.get(),'server': self.server_entry.get(),'port': int(self.port_entry.get())}))
        validate_button.pack(pady=25)

    
    def validateConfig(self, text):
        self.controller.frames[PageMain].setData(text)
        self.controller.frames[PageMain].getData(text)
        self.controller.showFrame(PageMain)
        

class PageMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.chat_box = scrolledtext.ScrolledText(self, state='disabled')
        self.chat_box.configure(font=("Courrier", 16))
        self.chat_box.grid(column=0, row=1, sticky='w', columnspan=4)    

        self.text_box = tk.Entry(self)
        self.text_box.grid(column=0, row=2,sticky="NSEW",pady=10,padx=(10,0))

        btn_send = Button(self, text="Send Message", font=("Courrier", 12), bg="royalblue", fg="white", 
                                            command=lambda: self.sendMsg({'msg': self.text_box.get(),}))                                                 
        btn_send.grid(column=1,row=2)
    
        btn_exit = tk.Button(self, text="Quitter", font=("Courrier", 12), bg="crimson", fg="white", width=10, command=self.quit)
        btn_exit.grid(column=4,row=2)

    def getData(self,data):
        username = data['username']

    def setData(self, data):
        self.client = Client(data['username'], data['server'], data['port'])
        self.client.listen(self.handle)

    def sendMsg(self, data):
        self.client.send(data['msg'])

    def handle(self, msg):
        self.chat_box.configure(state='normal')
        self.chat_box.insert(tk.END, msg + '\n')
        self.chat_box.configure(state='disabled')

if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()
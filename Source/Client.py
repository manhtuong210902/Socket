import json
from os import error
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import socket
from tkinter.constants import W


HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"

LOGIN = "login"
REGISTER = "register"
SEARCH = "search"
DISCONNECT="disconnect"
CONNECT="connect"
DISCONNECT_ALL="disconnect all clients"

def btn_clicked():
    print("Button Clicked")

def sendList(client, list):

    for item in list:
        client.sendall(item.encode(FORMAT))
        #wait response
        client.recv(1024)

    msg = "end"
    client.sendall(msg.encode(FORMAT))

def stringDay(str):
    newStr = ""
    for i in range(len(str)):
        if(str[i].isnumeric()):
            newStr += str[i]
    if(len(newStr) >= 7):
        day = newStr[:2]
        month = newStr[2:4]
        year = newStr[4:]
        newStr = year + month + day
    return newStr
        
class LoginFrame(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)
        self.configure(bg = "#ffffff")
        #khởi tạo với login
        canvas = tk.Canvas(
            self,
            bg = "#ffffff",
            height = 561,
            width = 473,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"image01/background.png")
        self.background = canvas.create_image(
            214.0, 379.0,
            image=self.background_img)

        #import ảnh button sign up
        self.img0 = tk.PhotoImage(file = f"image01/img0.png")
        #tạo button
        self.button_Register = tk.Button(
            self,
            image = self.img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: appController.showFrame(RegisterFrame),
            relief = "flat")
        #hiện button lên màn hình
        self.button_Register.place(
            x = 91, y = 374,
            width = 290,
            height = 24)

        #tạo khung nhập username
        self.entry0_img = tk.PhotoImage(file = f"image01/img_textBox0.png")
        self.entry0_bg = canvas.create_image(
            236.5, 262.5,
            image = self.entry0_img)

        self.entry_username = tk.Entry(
            self,
            bd = 0,
            bg = "#ebe7e7",
            font=('calibre',11,'normal'),
            highlightthickness = 0)

        self.entry_username.place(
            x = 113.0, y = 238,
            width = 247.0,
            height = 47)

        #tạo khung nhập mật khẩu
        self.entry1_img = tk.PhotoImage(file = f"image01/img_textBox1.png")
        self.entry1_bg = canvas.create_image(
            232.5, 347.5,
            image = self.entry1_img)

        self.entry_password = tk.Entry(
            self,
            bd = 0,
            bg = "#ebe7e7",
            font=('calibre',11,'normal'),
            highlightthickness = 0)

        self.entry_password.place(
            x = 109.0, y = 323,
            width = 247.0,
            height = 47)

        #tạo button đăng nhập
        self.img1 = tk.PhotoImage(file = f"image01/img1.png")
        self.button_log = tk.Button(
            self,
            image = self.img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: appController.loginIn(self, client),
            relief = "flat")

        self.button_log.place(
            x = 90, y = 444,
            width = 294,
            height = 49)
     
class RegisterFrame(tk.Frame):
    def __init__(self, parent, appController):
        #khởi tạo với Frame start page
        tk.Frame.__init__(self, parent)

        self.configure(bg = "#ffffff")

        canvas = tk.Canvas(
        self,
        bg = "#ffffff",
        height = 603,
        width = 473,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
        canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"image02/background.png")
        self.background = canvas.create_image(
            249.0, 286.5,
            image=self.background_img)

        self.entry0_img = tk.PhotoImage(file = f"image02/img_textBox0.png")
        self.entry0_bg = canvas.create_image(
            241.5, 195.5,
            image = self.entry0_img)

        self.entry_username = tk.Entry(
            self,
            bd = 0,
            bg = "#ebe7e7",
            font=('calibre',11,'normal'),
            highlightthickness = 0)

        self.entry_username.place(
            x = 118.0, y = 171,
            width = 247.0,
            height = 47)

        self.entry1_img = tk.PhotoImage(file = f"image02/img_textBox1.png")
        self.entry1_bg = canvas.create_image(
            237.5, 280.5,
            image = self.entry1_img)

        self.entry_password = tk.Entry(
            self,
            bd = 0,
            bg = "#ebe7e7",
            font=('calibre',11,'normal'),
            highlightthickness = 0)

        self.entry_password.place(
            x = 114.0, y = 256,
            width = 247.0,
            height = 47)

        self.entry2_img = tk.PhotoImage(file = f"image02/img_textBox2.png")
        self.entry2_bg = canvas.create_image(
            241.5, 372.5,
            image = self.entry2_img)

        self.entry_confirm = tk.Entry(
            self,
            bd = 0,
            bg = "#ebe7e7",
            font=('calibre',11,'normal'),
            highlightthickness = 0)

        self.entry_confirm.place(
            x = 118.0, y = 348,
            width = 247.0,
            height = 47)

        self.img0 = tk.PhotoImage(file = f"image02/img0.png")
        self.btn_signUp = tk.Button(
            self,
            image = self.img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: appController.signUp(self,client),
            relief = "flat")

        self.btn_signUp.place(
            x = 90, y = 429,
            width = 294,
            height = 49)

        self.img1 = tk.PhotoImage(file = f"image02/img1.png")
        self.btn_return = tk.Button(
            self,
            image = self.img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: appController.showFrame(LoginFrame),
            relief = "flat")

        self.btn_return.place(
            x = 90, y = 498,
            width = 294,
            height = 49)

class HomeFrame(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)
        self.configure(bg = "#ffffff")
        canvas = Canvas(
            self,
            bg = "#ffffff",
            height = 143,
            width = 976,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        self.background_img = PhotoImage(file = f"image03/background.png")
        self.background = canvas.create_image(
            367.0, -218.5,
            image=self.background_img)

        self.entry0_img = PhotoImage(file = f"image03/img_textBox0.png")
        self.entry0_bg = canvas.create_image(
            150.5, 102.0,
            image = self.entry0_img)

        self.entry_type = Entry(
            self,
            bd = 0,
            bg = "#e5e7e9",
            font=('calibre',11,'normal'),
            highlightthickness = 0)

        self.entry_type.place(
            x = 42.0, y = 78,
            width = 217.0,
            height = 46)

        self.entry1_img = PhotoImage(file = f"image03/img_textBox1.png")
        self.entry1_bg = canvas.create_image(
            425.5, 101.0,
            image = self.entry1_img)

        self.entry_day = Entry(
            self,
            bd = 0,
            bg = "#e5e7e9",
            font=('calibre',11,'normal'),
            highlightthickness = 0)

        self.entry_day.place(
            x = 317.0, y = 77,
            width = 217.0,
            height = 46)

        self.img0 = PhotoImage(file = f"image03/img0.png")
        self.btn_search = Button(
            self,
            image = self.img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: appController.searchGold(self,client),
            relief = "flat")

        self.btn_search.place(
            x = 573, y = 78,
            width = 71,
            height = 57)

        self.img1 = PhotoImage(file = f"image03/img1.png")
        self.btn_logout = Button(
            self,
            image = self.img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: appController.showFrame(LoginFrame),
            relief = "flat")

        self.btn_logout.place(
            x = 657, y = 76,
            width = 162,
            height = 57)
        
        #=== table frame ===
        self.Table_Frame = Frame(self, bd = 4, relief="ridge", bg="#01458E") #bg = "màu"
        self.Table_Frame.place(x = 18, y = 160, width=940, height=510)

        self.scrollx = Scrollbar(self.Table_Frame, orient=HORIZONTAL)
        self.scrolly = Scrollbar(self.Table_Frame, orient=VERTICAL)

        self.Table = ttk.Treeview(self.Table_Frame, columns=(1,2,3,4,5,6), show="headings",xscrollcommand=self.scrollx.set, yscrollcommand=self.scrolly.set)
        # self.scrollx.pack(side=BOTTOM, fill=X)
        self.scrolly.pack(side=RIGHT, fill=Y)
        # self.scrollx.config(command=self.Table.xview)
        self.scrolly.config(command=self.Table.yview)


        self.Table.heading(1, text="ID")
        self.Table.heading(2, text="TYPE")
        self.Table.heading(3, text="SELL")
        self.Table.heading(4, text="BUY")
        self.Table.heading(5, text="COMPANY")
        self.Table.heading(6, text="BRAND")

        
        self.Table.column(1,width=120)
        self.Table.column(2,width=120)
        self.Table.column(3,width=120)
        self.Table.column(4,width=120)
        self.Table.column(5,width=120)
        self.Table.column(6,width=120)

        
        self.Table.pack(fill=BOTH, expand=1)

class ErrorFrame(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)
        self.configure(bg = "#ffffff")
        canvas = Canvas(
            self,
            bg = "#ffffff",
            height = 445,
            width = 360,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        self.background_img = PhotoImage(file = f"image04/background.png")
        self.background = canvas.create_image(
            121.0, 152.0,
            image=self.background_img)

class StartFrame(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)
        self.configure(bg = "#ffffff")
        canvas = Canvas(
        self,
        bg = "#ffffff",
        height = 334,
        width = 312,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
        canvas.place(x = 0, y = 0)

        self.background_img = PhotoImage(file = f"image06/background.png")
        self.background = canvas.create_image(
            75.5, 148.5,
            image=self.background_img)

        self.img0 = PhotoImage(file = f"image06/img0.png")
        self.b0 = Button(
            self,
            image = self.img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda:appController.connectToSever(self,client),
            relief = "flat")

        self.b0.place(
            x = 53, y = 236,
            width = 206,
            height = 49)

        self.entry0_img = PhotoImage(file = f"image06/img_textBox0.png")
        self.entry0_bg = canvas.create_image(
            156.0, 102.5,
            image = self.entry0_img)

        self.entryIPaddr = Entry(
            self,
            bd = 0,
            bg = "#ebe7e7",
            font=('calibre',11,'normal'),
            highlightthickness = 0)

        self.entryIPaddr.place(
            x = 59.0, y = 78,
            width = 194.0,
            height = 47)

        self.entry1_img = PhotoImage(file = f"image06/img_textBox1.png")
        self.entry1_bg = canvas.create_image(
            156.0, 181.5,
            image = self.entry1_img)

        self.entryPort = Entry(
            self,
            bd = 0,
            bg = "#ebe7e7",
            font=('calibre',11,'normal'),
            highlightthickness = 0)

        self.entryPort.place(
            x = 59.0, y = 157,
            width = 194.0,
            height = 47)

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("My App")
        self.geometry("500x500")
        self.resizable(width=False, height=False)
        #self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = tk.Frame()
        container.configure(bg="#ffffff")

        container.pack(side="top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW",lambda: self.closing(client))
        self.frames = {}
        for F in (LoginFrame, HomeFrame, RegisterFrame,ErrorFrame,StartFrame):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame 
        self.showFrame(StartFrame)
        
    def showFrame(self, FrameClass):
        frame = self.frames[FrameClass]
        frame = self.frames[FrameClass]
        if(FrameClass == LoginFrame):
            self.title("LOGIN")
            self.geometry("473x561")
        elif(FrameClass == RegisterFrame):
            self.title("REGISTER")
            self.geometry("473x603")
        elif(FrameClass == ErrorFrame):
            self.title("404")
            self.geometry("360x445")
        elif(FrameClass == StartFrame):
            self.title("CONNECT")
            self.geometry("312x334")
        else:
            self.title("HOME")
            self.geometry("976x700")
        frame.tkraise()
    def loginIn(self, curFrame, sck:socket):
        try:
            account = []
            username = curFrame.entry_username.get()
            password = curFrame.entry_password.get()

            print(username, password)
            if(username == "" or password == ""):
                messagebox.showwarning("Thông báo", "không được để trống")
                print("nhập lại hộ")
                return
             #bỏ username và password vào list
            account.append(username)
            account.append(password)

            #cho option là Login gửi đến sever
            option = LOGIN
            sck.sendall(option.encode(FORMAT))
            sck.recv(1024)

            #gửi cho sever list account
            sendList(sck, account)

            #nhận phản hồi từ server và đưa ra thông báo
            validCheck = sck.recv(1024).decode(FORMAT)
            if(validCheck == "True"):
                print("đăng nhập thành công")
                # messagebox.showinfo("Thông báo","Đăng nhập thành công")
                self.showFrame(HomeFrame)
            else:
                messagebox.showerror("Thông báo","Tài khoản hoặc mật khẩu không đúng")
                print("đăng nhập thất bại")
            
        except:
            self.showFrame(ErrorFrame)
            print("Error: Server is not responding")     
    def signUp(self, curFrame ,sck:socket):
        try:
            account = []
            username = curFrame.entry_username.get()
            password = curFrame.entry_password.get()
            confirm = curFrame.entry_confirm.get()
            print(username, password, confirm)
            if(username == "" or password == "" or confirm == ""):
                messagebox.showwarning("Thông báo", "Không được để trống")
                return
            elif(password != confirm):
                messagebox.showwarning("thông báo", "nhập lại mất khẩu không chính xác")
                return
            
             #bỏ username và password vào list
            account.append(username)
            account.append(password)

            #cho option là Login gửi đến sever
            option = REGISTER
            sck.sendall(option.encode(FORMAT))
            sck.recv(1024)

            #gửi cho sever list account
            sendList(sck, account)

            #nhận phản hồi từ server và đưa ra thông báo
            validCheck = sck.recv(1024).decode(FORMAT)
            if(validCheck == "True"):
                messagebox.showinfo("Thông báo","Đăng kí thành công")
            else:
                messagebox.showwarning("Thông báo","Tài khoản đã tồn tại")
            
        except:
            self.showFrame(ErrorFrame)
            print("Error: Server is not responding")
    def searchGold(self, curFrame, sck:socket):
        try:
            textSearchType = curFrame.entry_type.get()
            textSearchDay = curFrame.entry_day.get()
            if (textSearchType == "" and textSearchDay == ""):
                return
            textSearchDay = stringDay(textSearchDay)
            print(textSearchDay)
            if(textSearchDay == ""):
                messagebox.showwarning("thông báo","chưa nhập ngày")
                return
            if(textSearchType == ""):
                messagebox.showwarning("thông báo","chưa nhập loại vàng")
                return
            
            option = SEARCH
            sck.sendall(option.encode(FORMAT))
            sck.recv(1024)

            textSearch = []
            textSearch.append(textSearchType)
            textSearch.append(textSearchDay)

            sendList(sck, textSearch)

            newMsg = sck.recv(100000).decode(FORMAT)

            if(newMsg == "false"):
                curFrame.Table.delete(*curFrame.Table.get_children())
                messagebox.showinfo("Thông báo","Không tìm thấy thông tin")
                return
            else:
                list = json.loads(newMsg)
                curFrame.Table.delete(*curFrame.Table.get_children())
                for item in list:
                    curFrame.Table.insert(parent='', index='end',
                    values=(item['id'], item['type'], item['sell'], item['buy'], item['company'],item['brand']))

        except:
            self.showFrame(ErrorFrame)
            print("ERROR")
    def closing(self, sck:socket):
        if messagebox.askokcancel("Thông báo","Bạn có muốn ngừng kết nối với SERVER"):
            try:    
                #gửi thông báo ngừng kết nối với server
                msg=DISCONNECT
                sck.sendall(msg.encode(FORMAT))
                sck.recv(1024).decode(FORMAT)

                sck.sendall(str(sck.getsockname()).encode(FORMAT))
                sck.close()
                self.destroy()
            except:
                sck.close()
                self.destroy()
        return False
    def connectToSever(self, curFrame, sck:socket):
        IPaddr = curFrame.entryIPaddr.get()
        Port = int(curFrame.entryPort.get())

        try:
            sck.connect((IPaddr,Port))
            msg = CONNECT
            sck.sendall(msg.encode(FORMAT))
            sck.recv(1024).decode(FORMAT)

            sck.sendall(str(client.getsockname()).encode(FORMAT))
            self.showFrame(LoginFrame)
        except:
            messagebox.showinfo("Thông báo","sever chưa được khởi chạy")

class ErrorPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("ERROR FAGE")
        self.geometry("360x445")
        self.configure(bg = "#ffffff")
        self.resizable(False, False)
        canvas = tk.Canvas(
            self,
            bg = "#ffffff",
            height = 445,
            width = 360,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"image04/background.png")
        self.background = canvas.create_image(
            121.0, 152.0,
            image=self.background_img)

#--------main--------#
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
app = App()
try:
    app.mainloop()
except:
    app.update()
    app.destroy()
    app2 = ErrorPage()
    app2.mainloop()
    print("Error: server is not responding")
    client.close()
finally:
    client.close()

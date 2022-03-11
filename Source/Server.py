import socket 
import threading #thư viện để kết nối đa luồng
import json
import time
import requests
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

HOST = "127.0.0.1" 
SERVER_PORT = 65432 
FORMAT = "utf8"

LOGIN = "login"
REGISTER = "register"
SEARCH = "search"
DISCONNECT_ALL="disconnect all clients"
DISCONNECT="disconnect"
CONNECT="connect"
END = "x"
API = "https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date"
#hàm nhận phản hồi từ phía client là một cái list[]
def recvList(conn):
    list = []

    item = conn.recv(1024).decode(FORMAT)

    while (item != "end"):
        
        list.append(item)
        #response
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    
    return list

#gửi list golds 
def sendListGolds(conn, list):
    data = json.dumps(list)
    conn.sendall(data.encode(FORMAT))

#đọc file dữ liệu từ web
def getDataFromApi(api):
    reponse= requests.get(api)
    reponse.encoding = 'utf-8-sig'
    json_data = reponse.json()
    dataGolds = json_data["golds"]

    fileOut = open("data.json","w")
    fileOut.write(json.dumps(dataGolds, indent = 4))
    fileOut.close()

#lấy dữ liệu từ file
def getData():
    fileIn = open("data.json","r")
    data = json.loads(fileIn.read())
    fileIn.close()
    return data

#hàm tìm kiếm 
def listLookFor(textSearch):
    data = getData()
    listItem = []
    for itemX in data:
        if(textSearch[1] == itemX['date']):
            for itemY in itemX['value']:
                if(textSearch[0] == itemY['company'] or textSearch[0] == itemY['type']):
                    listItem.append(itemY)
    
    if(len(listItem) == 0):
        return "false"
    else:
        return listItem

#hàm nhận phản hồi search
def searchGolds(conn):
    textSearch = recvList(conn)
    print(textSearch)

    list = listLookFor(textSearch)

    if(list == "false"):
        conn.sendall(list.encode(FORMAT))
    else:
        conn.sendall(json.dumps(list).encode(FORMAT))

#hàm kiểm tra tên đăng nhập và mật khẩu có đúng khi đăng nhập
def checkLogin(username, password):
    fileIn = open('user.json',"r") #đọc json
    dataAccount = json.loads(fileIn.read()) #cho dữ liệu ra
    fileIn.close()
    for user in dataAccount:
        if(username == user['username'] and password == user['password']):
            return True
    return False

#hàm sever xứ lý khi nhận phản hồi là đăng nhập
def serverHandleAccount(conn):
    #nhận account từ client
    clientAccount = recvList(conn)
    print(clientAccount[0],clientAccount[1])
    check = checkLogin(clientAccount[0],clientAccount[1])
    msg = ""
    if(check == True):
        msg = "True"
        print("logged in successfully")
    else:
        msg = "False"
        print("logged in failed")
    conn.sendall(msg.encode(FORMAT))

#kiểm tra tải khoản đã tồn tại chưa
def checkSignUp(newClientAccount):
    fileIn = open('user.json',"r") #đọc json
    dataAccount = json.loads(fileIn.read()) #cho dữ liệu ra
    fileIn.close()
    for user in dataAccount:
        if(newClientAccount[0] == user["username"] and newClientAccount[1] == user["password"]):
            return False
    return True

#hàm sever thêm tài khoản khi nhận phản hồi là đăng kí
def createNewAccount(conn):
    fileIn = open('user.json',"r")
    dataAccount = json.loads(fileIn.read())
    fileIn.close()
    newClientAccount = recvList(conn)
    check = checkSignUp(newClientAccount)
    msg = ""
    if(check == True):
        fileOut = open('user.json',"w")
        x = {
            "username":newClientAccount[0],
            "password":newClientAccount[1]
        }
        dataAccount.append(x)
        fileOut.write(json.dumps(dataAccount, indent= 4))  
        fileOut.close()
        msg = "True"
        print("register succesfully")
    else:
        msg = "False"
        print("register failed")
    conn.sendall(msg.encode(FORMAT))

#hàm connect 1 client live vào file json
def connectClient(conn):
    fileIn = open('client_live.json',"r")
    dataClientLive = json.loads(fileIn.read())
    fileIn.close()
    msg=conn.recv(1024).decode(FORMAT) # nhận địa chỉ client
    newClient={
        "client": msg,
        "connect":"connected"
    }
    fileOut = open('client_live.json',"w")
    dataClientLive.append(newClient)
    fileOut.write(json.dumps(dataClientLive, indent= 4))  
    fileOut.close()
    print(newClient)

#hàm disconnect 1 client 
def disconnectClient(conn):
    fileIn = open('client_live.json',"r")
    dataClientLive = json.loads(fileIn.read())
    fileIn.close()
    msg=conn.recv(1024).decode(FORMAT)  # nhận địa chỉ client
    
    # messagebox.showinfo("",msg +"ngừng kết nối")
    for client in dataClientLive:
        if client['client'] == msg:
            dataClientLive.remove(client)
            break
    fileOut = open('client_live.json',"w")
    fileOut.write(json.dumps(dataClientLive, indent= 4))  
    fileOut.close()

#hàm xử lý client
def handleCLient(conn:socket, addr):
    print("Client", addr, "connected")
    print("conn:",conn.getsockname())

    option = None
    while (option != END):
        option = conn.recv(1024).decode(FORMAT)
        if option == LOGIN:
            conn.sendall(option.encode(FORMAT))
            serverHandleAccount(conn)
        elif option == REGISTER:
            conn.sendall(option.encode(FORMAT))
            createNewAccount(conn)
        elif option == SEARCH:
            conn.sendall(option.encode(FORMAT))
            searchGolds(conn)
        elif option == CONNECT:
            conn.sendall(option.encode(FORMAT))
            connectClient(conn)
        elif option == DISCONNECT:
            conn.sendall(option.encode(FORMAT))
            disconnectClient(conn)
    print("client ",addr," finished" )
    print(conn.getsockname(), " closed")
    conn.close()

#run sever
def runServer():
    try:
        print(HOST)
        print("Waiting for Client")
        check=True
        while check==True:           
            try:
                print("enter while loop")
                conn, addr = s.accept()          
                thr = threading.Thread(target=handleCLient, args=(conn,addr))
                thr.daemon = True
                thr.start()  
                print("end main-loop")
            except:
                check=False
                print("Đã ngắt kết nối")
                s.close()             
    except KeyboardInterrupt:
        print("error")
        s.close()
    finally:
        s.close()
        print("end")

#cập nhật dữ liệu 30' một lần
def updateData():
    while (True):
        print("get data successfully")
        getDataFromApi(API)
        time.sleep(1800)

#hàm test button
def btn_clicked():
    print("Button Clicked")


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("SERVER")
        self.geometry("508x426")
        self.configure(bg = "#ffffff")
        self.resizable(False, False)      
        self.protocol("WM_DELETE_WINDOW", self.closing)

        canvas = Canvas(
            self,
            bg = "#ffffff",
            height = 426,
            width = 508,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        self.background_img = tk.PhotoImage(file = f"image05/background.png")
        self.background = canvas.create_image(
            249.5, 47.0,
            image=self.background_img)

        self.img0 = tk.PhotoImage(file = f"image05/img0.png")
        self.b0 = tk.Button(
            image = self.img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda:self.showClient(),
            relief = "flat")

        self.b0.place(
            x = 150, y = 341,
            width = 202,
            height = 63)

        #=== table frame ===
        self.Table_Frame = tk.Frame(self, bd = 4, relief="ridge", bg="#01458E") #bg = "màu"
        self.Table_Frame.place(x = 8, y = 90, width=492, height=250)

        self.scrollx = tk.Scrollbar(self.Table_Frame, orient=HORIZONTAL)
        self.scrolly = tk.Scrollbar(self.Table_Frame, orient=VERTICAL)

        self.Table = ttk.Treeview(self.Table_Frame, columns=(1,2,3), show="headings",xscrollcommand=self.scrollx.set, yscrollcommand=self.scrolly.set)
        # window.scrollx.pack(side=BOTTOM, fill=X)
        self.scrolly.pack(side=RIGHT, fill=Y)
        # window.scrollx.config(command=Table.xview
        self.scrolly.config(command=self.Table.yview)

        self.Table.heading(1, text="NO.")
        self.Table.heading(2, text="CLIENT")
        self.Table.heading(3, text="CONNECT")

        self.Table.column(1,width=120)
        self.Table.column(2,width=120)
        self.Table.column(3,width=120)

        self.Table.pack(fill=BOTH, expand=1)
        
    def showClient(self):
        fileIn = open('client_live.json',"r")
        dataClientLive = json.loads(fileIn.read())
        fileIn.close()
        self.Table.delete(*self.Table.get_children())
        id = 1
        for client in dataClientLive:
            self.Table.insert(parent='', index='end',
            values=(id, client["client"], client["connect"]))
            id += 1
    def closing(self):
        if messagebox.askokcancel("Quit", "Bạn có muốn dừng sever?"):
            try:
                dataClientLive = []
                fileOut = open('client_live.json',"w")
                fileOut.write(json.dumps(dataClientLive, indent= 4))  
                fileOut.close()
                self.destroy()
            except:
                self.destroy()
        return False
#----- main -----#
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((HOST, SERVER_PORT))
s.listen(1)

sThread = threading.Thread(target=runServer)
sThread.daemon = True 
sThread.start()

tThread = threading.Thread(target=updateData)
tThread.daemon = True
tThread.start()

app = App()
app.mainloop()


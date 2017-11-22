import socket

class Client():
    def __init__(self):
        self.socket = socket.socket()
        self.name = ""

    def connectServer(self, host, port):
        # CONNECT
        self.socket.connect((host,port))
        #Receive server information
        info = self.socket.recv(1024).decode()
        print("Current server: " + info.split(" ")[0] + "/" + info.split(" ")[1])
        # SETUP NAME
        print("Input user name: ")
        while True:
            name = input()
            self.socket.send(name.encode())
            res = self.socket.recv(1024).decode()
            if res == "1":
                print( "Registered to server")
                self.name = name
                break
            elif res == "0":
                print( "Syntax error")
            else:
                print( "Username is used")
            print( "Please choose other username: ")
        #Wait for others player
        while True:
            count = self.socket.recv(1024).decode()
            if (count != "Done"):
                print((str(count) + "/" + "3 player connected to server"))
            else:
                print("All players connected. Game will start in 3s")


fClient = Client()
fClient.connectServer(socket.gethostname(),1234)
        
import socket

class Client():
    def __init__(self):
        self.socket = socket.socket()
        self.name = ""
        self.SCORE = []
        self.LNUM = 0

    def connectServer(self, host, port):
        # CONNECT
        self.socket.connect((host,port))
        #Receive server information
        info = self.socket.recv(1024).decode()
        print("Current server: " + info.split(" ")[0] + "/" + info.split(" ")[1])
        # SETUP NAME
        print("Input user name: ")
        while True:
            name = raw_input()
            self.socket.send(name.encode())
            res = self.socket.recv(1024).decode()
            if res == "e0":
                print( "Syntax error")
            elif res == "e1":
                print( "Username is used")
            else:
                print( "Registered to server")
                self.name = name
                self.LNUM = int(res)
                break
            print( "Please choose other username: ")
        #Wait for others player
        while True:
            count = self.socket.recv(1024).decode()
            print((str(count) + "/" + "3 player connected to server"))
            if (int(count) == PNUM):
                print("All players connected. Game will start in 3s")
                break

    def initGame(self):
        list_player = self.socket.recv(1024)
        for player in list_player.split():
            self.SCORE.append([player,0])

        print self.SCORE


PNUM = 3
fClient = Client()
fClient.connectServer(socket.gethostname(),12345)
fClient.initGame()
        
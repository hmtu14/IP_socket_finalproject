import socket
# import Tkinter as tk
import re
import threading
import time
from random import randint
import os



def debug(text):
    print text

class Server():
    #Check name, return 0 if syntax error, 1 if duplicated, 2 if OK
    def checkName(self, name):
            pattern = re.compile("([^a-zA-Z0-9])+")
            if (pattern.search(name) != None):
                return 0
            if (len(name) > 10):
                return 0
            if (name in self.CONNECTION):
                return 1
            return 2

    #Count the number of player each 1s, close if enough
    class countPlayerThread(threading.Thread):
        def __init__(self, server):
            threading.Thread.__init__(self)
            self.PCount = 0
            self.Server = server

        def run(self):
            while True:
                time.sleep(1)
                if (len(self.Server.CONNECTION) != self.PCount):
                    for name in self.Server.CONNECTION:
                        self.Server.CONNECTION[name][0].send(str(len(self.Server.CONNECTION)).encode())
                    self.PCount = len(self.Server.CONNECTION)
                    if (self.PCount == self.Server.PNUM):
                        socket.socket().connect((socket.gethostname(),12345))
                        self.Server.socket.close()
                        return


    class setUpConnectionThread(threading.Thread):
        def __init__(self, server, connect):
            threading.Thread.__init__(self)
            self.connect = connect
            self.Server = server
            
        def run(self):
            # Sent server information (Current number of player and Max number of player)
            self.connect.send((str((len(self.Server.CONNECTION))) + " " + str(self.Server.PNUM)).encode())
            #Wait for player to register
            while True:
                try:
                    name = self.connect.recv(1024).decode()
                except:
                    break
                #Check number of player
                if (len(self.Server.CONNECTION) == self.Server.PNUM):
                    self.connect.close()
                    break
                if (self.Server.checkName(name) == 2):
                    self.connect.send(str(self.Server.LNUM).encode())
                    self.Server.CONNECTION[name] = []
                    self.Server.CONNECTION[name].append(self.connect)
                    print ("Player " + name + " connected")
                    break
                elif self.Server.checkName(name) == 0:
                    self.connect.send("e0".encode())
                else:
                    self.connect.send("e1".encode())


    def __init__(self, host, port, PNUM):
        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.PNUM = PNUM
        self.CONNECTION = {}
        self.countPThred = Server.countPlayerThread(self)
        self.countPThred.start()
        self.connectLock = False
        self.SCORE = {}
        self.LNUM = randint(1,30)
        print("Created server")
    
    def openForConnection(self):
        self.socket.listen(5)
        print ("Waiting for player to connect ...")
        while (len(self.CONNECTION) < self.PNUM):
            try:
                connect, addr = self.socket.accept()
                setupThread = Server.setUpConnectionThread(self, connect)
                setupThread.start()
            except:
                print("All players connected. Game will start in 3s")

    def initGame(self):
        os.system("clear")
        print("List of player: ")
        list_player = " ".join(str(i) for i in self.CONNECTION.keys())
        for player in self.CONNECTION:
            print(player)
            self.SCORE[player] = 0
            self.CONNECTION[player][0].send(list_player)
            #nen dat them recv o day
        print ("Length: " + str(self.LNUM))
        for i in range(0,3):
            time.sleep(1)
            print (3-i)


    def startGame(self):
        while True:
            for player in self.CONNECTION:
                print (player + "'s turn ...")
                for t_player in self.CONNECTION:
                    self.CONNECTION[t_player][0].send(player.encode())
                point = self.CONNECTION[player][0].recv(1024).decode()
                #Kiem tra diem:
                if (self.SCORE[player] + int(point)) == self.LNUM:
                    for t_player in self.CONNECTION:
                        self.CONNECTION[t_player][0].send("win".decode())
                        self.CONNECTION[t_player][0].close()
                    print ("Player " + player + " won")
                    print ("The game will end in 3s ...")
                    exit()
                else:
                    #Update in server:
                    if (self.SCORE[player] + int(point)) < self.LNUM:
                        self.SCORE[player] += int(point)
                    #Update in client:
                    for t_player in self.CONNECTION:
                        self.CONNECTION[t_player][0].send(str(self.SCORE[player]).decode())
                        #Nen dat them recv o day
                    time.sleep(1)


if (__name__ == "__main__"):
    while True:
        print "Input Number of Player: "
        PNUM = raw_input()
        try:
            PNUM = int(PNUM)
            if (PNUM > 1 and PNUM < 9):
                break
        except:
            pass

    fServer = Server(socket.gethostname(),12345,PNUM)
    fServer.openForConnection()
    fServer.initGame()
    fServer.startGame()

import socket
from random import randint
import os

def debug(text):
    print "======"
    print text
    print "======"



class Client():
    def __init__(self):
        self.socket = socket.socket()
        self.name = ""
        self.SCORE = {}
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


    def printScore(self):
        for player in self.SCORE:
            print(player, self.SCORE[player])

    def initGame(self):
        os.system("cls")
        list_player = self.socket.recv(1024)
        for player in list_player.split():
            self.SCORE[player] = 0
        self.printScore()


    def startGame(self):
        while True:
            #Nhan ten player den luot tu server
            player = self.socket.recv(1024).decode()
            debug(player)
            if (player == self.name):
                #Neu la luot minh
                print "Your turn, press enter to roll ..."
                #Bug here, need to clear buffer
                raw_input()
                roll = randint(1,6)
                print ("You rolled " + str(roll) + " point" )
                self.socket.send(str(roll).encode())
            new_score = self.socket.recv(1024).decode()
            if (new_score == "win"):
                print ("Player " + player + " won")
                print ("The game will end in 3s ...")
                self.socket.close()
                exit()
            else:
                self.SCORE[player] = int(new_score)
            self.printScore()
            print "======================="
            print "Next turn"


PNUM = 3
fClient = Client()
fClient.connectServer(socket.gethostname(),12345)
fClient.initGame()
fClient.startGame()
        
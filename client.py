import socket




#INIT SOCKET
s = socket.socket()
host = socket.gethostname()
port = 1234
s.connect((host, port))


print "Input user name: "
while True:
    name = raw_input()
    s.send(name)
    res = s.recv(1024)
    if res == "1":
        print "Registered to server"
        break
    elif res == "0":
        print "Syntax error"
    else:
        print "Username is used"
    print "Please choose other username: "
while True:
    count = s.recv(1024)
    if (count != "Done"):
        print (str(count) + "/" + "3 player connected to server")
    else:
        s.close()
        break

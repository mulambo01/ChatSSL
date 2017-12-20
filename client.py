from thread import start_new_thread
import time, os
import socket, sys, ssl, commandlist

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if(len(sys.argv)<4):
    print "Use:", sys.argv[0],"SERVER PORT NICKNAME"
    quit()
host=sys.argv[1]
port=int(sys.argv[2])
conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    tcp=ssl.wrap_socket(conn,cert_reqs=ssl.CERT_REQUIRED, ca_certs='crt.pem')
except(IOError):
    print bcolors.FAIL+"ERROR: You don't have the file \"crt.pem\" in this directory."+bcolors.ENDC
    quit()
tcp.connect((host, port))
nick=sys.argv[3]
tcp.send(nick)
print bcolors.OKGREEN+"You are connected!"+bcolors.ENDC
def receive(tcp):
    while(1):
        msg=tcp.recv(10000)
        if not msg:
            print bcolors.FAIL+"The server crashes.\nCtrl+C and try again."+bcolors.ENDC
            break
        print bcolors.OKBLUE+msg+bcolors.ENDC

def main():
#thread to receive messages
    start_new_thread(receive,(tcp,))
    while(1):
        msg=raw_input()
        if msg in commandlist.list:
            c, m = commandlist.sendcommand(msg)
            if c == 1:
                tcp.send(m)
        elif msg[-4:len(msg)]=="/del":
            print bcolors.FAIL+bcolors.BOLD+"INPUT BUFFER IS CLEAN"+bcolors.ENDC+bcolors.ENDC
        elif not(msg in commandlist.avoid):
            tcp.send(msg)
try:
    main()
except(KeyboardInterrupt):
    print bcolors.FAIL+"Disconnected"+bcolors.ENDC
    quit()

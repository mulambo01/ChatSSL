#!/usr/bin/python2
import readline #this module improves the function raw_input()
from thread import start_new_thread
import signal, socket, sys, commandlist, os, ssl

PID=os.getpid()

class bcolors:
 HEADER = '\033[95m'
 OKBLUE = '\033[94m'
 OKGREEN = '\033[92m'
 WARNING = '\033[93m'
 FAIL = '\033[91m'
 ENDC = '\033[0m'
 BOLD = '\033[1m'
 UNDERLINE = '\033[4m'

try:
 host=sys.argv[1]
 port=int(sys.argv[2])
 nick=sys.argv[3]
except:
 print "Use:", sys.argv[0],"SERVER PORT NICKNAME"
 quit()
conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((host, port))
tcp=ssl.wrap_socket(conn)
tcp.getpeercert(True)

tcp.send(nick)
print bcolors.OKGREEN+"You are connected!"+bcolors.ENDC

def receive(tcp):
 while(1):
  msg=tcp.recv(10000)
  if not msg:
   print bcolors.FAIL+"The connection was closed."+bcolors.ENDC
   os.kill(PID, signal.SIGUSR1)
   break
  try:
   print bcolors.OKBLUE+msg+bcolors.ENDC
  except Exception as error:
   print "Error! "+str(error)

def main():
#thread to receive messages
 start_new_thread(receive, (tcp,))
 while(1):
  msg=raw_input()
  if msg in commandlist.list:
   c, m = commandlist.sendcommand(msg)
   if c == 1:
    tcp.send(m)
  elif msg[-4:len(msg)]=="/del":
   print bcolors.FAIL+bcolors.BOLD+"INPUT BUFFER IS CLEAN"+bcolors.ENDC+bcolors.ENDC
  elif not(msg in commandlist.avoid):
   try:
    tcp.send(msg)
   except Exception as error:
    print "Error! "+str(error)
try:
 main()
except(KeyboardInterrupt):
 print bcolors.FAIL+"Disconnected"+bcolors.ENDC
 tcp.close()
 quit()

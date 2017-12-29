#!/usr/bin/python2
import readline #this module improves the function raw_input()
from thread import start_new_thread
import signal, socket, sys, commandlist, os, ssl

PID=os.getpid()

class bcolors:
 HEADER = '\033[95m'
 BLUE = '\033[94m'
 GREEN = '\033[32m'
 RED = '\033[31m'
 YELLOW = '\033[33m'
 PINK = '\033[35m'
 WARNING = '\033[93m'
 ENDC = '\033[0m'
 BOLD = '\033[1m'
 UNDERLINE = '\033[4m'
 color=[BLUE, GREEN, YELLOW, BLUE, RED]

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

mark="-"
def findmark(msg, point):
 i=0
 while(msg[i]!=point):
  i=i+1
 return i

def call(msg):
 testmsg=msg+" end"
 if(len(testmsg.split(" "+nick+" "))>1):
  return 1
 else:
  return 0
def receive(tcp):
 while(1):
  msg=tcp.recv(10000)
  if not msg:
   print bcolors.RED+"The connection was closed."+bcolors.ENDC
   os.kill(PID, signal.SIGUSR1)
   break
  try:
   msgtp=int(msg.split(mark)[0])
   msg=msg[findmark(msg, mark)+1::]
   if(call(msg)):
    msg=msg+"\a"
   print bcolors.color[msgtp]+msg+bcolors.ENDC
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
   print bcolors.RED+bcolors.BOLD+"INPUT BUFFER IS CLEAN"+bcolors.ENDC+bcolors.ENDC
  elif not(msg in commandlist.avoid):
   try:
    tcp.send(msg)
   except Exception as error:
    print "Error! "+str(error)
try:
 main()
except(KeyboardInterrupt):
 print bcolors.RED+"Disconnected"+bcolors.ENDC
 tcp.close()
 quit()

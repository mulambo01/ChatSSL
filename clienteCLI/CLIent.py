#!/usr/bin/python2
import readline #this module improves the function raw_input()
import signal, socket, sys, os, ssl
from thread import start_new_thread
from curses import wrapper
import ui
from ui import ChatUI
from datetime import datetime

PID=os.getpid()
commandlist=['/who','/exit']
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

def getclock():
 time=datetime.now()
 clock="["+str(time.hour+100)[1::]+":"+str(time.minute+100)[1::]+":"+str(time.second+100)[1::]+"] "
 return clock

def receive(tcp, ui):

 while(1):
  msg=tcp.recv(10000)
  if not msg:
   print bcolors.FAIL+"The connection was closed."+bcolors.ENDC
   os.kill(PID, signal.SIGUSR1)
   break
  try:
   if(msg.split("\n")[0]=="Users:"):
    usrlst=msg.split("\n")
    ui.userlistbuffer_update(usrlst)
   else:
    ui.chatbuffer_add(msg)
  except Exception as error:
   ui.chatbuffer_add("Error! "+str(error))

def main(stdscr):
#thread to receive messages
 stdscr.clear()
 ui=ChatUI(stdscr)
 ui.chatbuffer_add("You are connected!")
 start_new_thread(receive,(tcp, ui))
 while(1):
  msg=ui.wait_input("["+nick+"]"+": ")
  try:
   time=getclock()
   if not msg in commandlist:
    ui.chatbuffer_add(time+nick+": "+msg)
   tcp.send(msg)
  except Exception as error:
   print "Error! "+str(error)
try:
 wrapper(main)
except(KeyboardInterrupt):
 print bcolors.FAIL+"Disconnected"+bcolors.ENDC
 tcp.close()
 quit()

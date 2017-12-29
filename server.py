#!/usr/bin/python2
from datetime import datetime
from thread import start_new_thread
import socket, sys, time, os, ssl
path=os.path.realpath(__file__)
path=path.split("/")
path[-1]=""
path="/".join(path)
"""
messages type:
0 - normal message
1 - new user in room
2 - user exit
3 - userlist
4 - system message
"""
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

KEYFILE=path+'keys/key.pem'
CERTFILE=path+'keys/crt.pem'

try:
 host=''
 port=int(sys.argv[1])
except:
 print "Use:", sys.argv[0],"PORT"
 quit()
try:
 context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
 context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
except:
 print "You need to generate your own key, to do that you need the package \"openssl\" and run:\n"+bcolors.OKBLUE+"openssl genrsa -out key.pem && yes '' | openssl req -new -x509 -key key.pem -out crt.pem"+bcolors.ENDC
 quit()

connect=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig=(host, port)
connect.bind(orig)
connect.listen(1)

connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#max number of connetions
limit=200
con=["0"]*limit
client=["0"]*limit
nick=["0"]*limit

def getclock():
 time=datetime.now()
 clock="["+str(time.hour+100)[1::]+":"+str(time.minute+100)[1::]+":"+str(time.second+100)[1::]+"] "
 return clock
#procedure to finish client connections
def down(index):
 clock=getclock()
 print clock+"Client "+str(index)+" fell."
#the value 1 indicates that the socket was in using but now is free, 0 means that the socket is virgin
 msg=clock+"User "+nick[index]+" exits."
 try:
  con[index].close()
 except Exception as error:
  print "Error! "+str(error)
 con[index]="1"
 client[index]="1"
 nick[index]="1"
 j=0
 while(j<limit and con[j]!="0"):
  if(con[j]!="1" and j!=index):
   try:
    msgtp="2-"
    con[j].sendall(msgtp+msg)
   except Exception as error:
    print "Error! "+str(error)
  j=j+1

def is_number(var):
  try:
    float(var)
    return True
  except:
    return False

#function that will manage the connection called by the index
#all the connections will have a dedicated thread running this function
def receive(index):
 try:
  conn=con[index]
  
  nick[index]=conn.recv(50)
  Nick=nick[index]
  if(is_number(Nick)):
   msgtp="4-"
   conn.sendall(msgtp+"Your nick can\'t be a number!")
   down(index)
  print client[index],Nick,index
  j=0
  while(j<limit and con[j]!="0"):
   clock=getclock()
   if(con[j]!="1" and j!=index):
    message=clock+"User "+Nick+" came into the room."
    msgtp="1-"
    con[j].sendall(msgtp+message)
   j=j+1
  msgtp="4-"
  conn.sendall(msgtp+"You are connected!")
  while(1):
   msg=str(conn.recv(10000))
   if not msg:
    down(index)
    break
#if the message is /who, all the users in the room will be listed
   if(msg=="/who"):
    j=0
    output="Users:"
    while(nick[j]!="0"):
     if(nick[j]!="1"):
      output=output+"\n"+nick[j]
     j=j+1
    msgtp="3-"
    conn.sendall(msgtp+str(output))
   else:
    clock=getclock()
    msg=clock+Nick+": "+msg
    print msg, index
    j=0
    while(j<limit and con[j]!="0"):
     if(con[j]!="1" and j!=index):
      msgtp="0-"
      con[j].sendall(msgtp+msg)
     j=j+1
 except Exception as error:
  try:
   down(index)
   print "Error! "+str(error)
  except Exception as error:
   print "Error! "+str(error)

def main():
 print bcolors.OKGREEN+"The server is ready!"+bcolors.ENDC
 i=0
#this variable will be used to save cpu
 cpusave=0
 while(1):
  if(con[i]=="0" or con[i]=="1"):
   time.sleep(3)
   con[i], client[i]=connect.accept()
   try:
    con[i]=context.wrap_socket(con[i], server_side=True)
   except:
    print "SSL ERROR"
    error="Problem with the SSL connection."
    msgtp="4-"
    con[i].sendall(msgtp+error)
    con[i].close()
    con[i]=client[i]="0"
    continue
   start_new_thread(receive,(i,))
   if(i==limit-1):
    i=0
   else:
    i=i+1
  elif(i<limit-1):
   i=i+1
  elif(cpusave==0):
   i=0
   cpusave=1
  else:
#here is where the variable act, after a complete loop in the list of connections
#if no address is free, the program will sleep for 2 seconds before repeat the cicle
   i=0
   cpusave=0
   time.sleep(2)

try:
 main()
except(KeyboardInterrupt):
 print "Closing the connection."
 i=0
 while(con[i]!="0" and i<limit):
  if(con[i]!="1"):
   try:
    con[i].shutdown(socket.SHUT_RDWR)
    con[i].close()
   except Exception as error:
    print "Error! "+str(error)
  i=i+1
 connect.shutdown(socket.SHUT_RDWR)
 connect.close()
 quit()

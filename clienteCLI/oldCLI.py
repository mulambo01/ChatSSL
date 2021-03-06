#!/usr/bin/python2
from thread import start_new_thread
import time, socket, sys, commandlist, ast, os
path=os.path.realpath(__file__)
path=path.split("/")
path[-1]=""
path="/".join(path)
sys.path.append(path+'pycrypto-2.6.1/lib/python2.7/site-packages/')
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from curses import wrapper
from ui import ChatUI
from datetime import datetime
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
sizekey=128

try:
 arq=open(path+"clientKey/key.pem", "r")
 key=arq.read()
 key=RSA.importKey(key)
 publickey=key.publickey()
 publicascii=str(publickey.exportKey())
 arq.close()
except:
 print "If you want to use your own key, save the private key as \"key.pem\" in the directory called \"clientKey\".\nThe default size is 1024 bits."
 print "You can generate your own key using the program \"openssl\". When you have it installed in your machine, run \"openssl genrsa -out key.pem 1024\" and put the file in the correct directory."
 random_generator = Random.new().read
 key = RSA.generate(sizekey*8, random_generator)
 publickey = key.publickey()
 publicascii=str(publickey.exportKey())
#the key has a limit of 128 bytes, so to solve that problem, the big messages need
#to be splited, encrypted singly and reconnected with this spacer in the middle
spacer="@@@"

def decrypt(msg):
 newmsg=msg.split(spacer)
 decrypted=""
 i=0
 while(i<len(newmsg)):
  decrypted = decrypted+str(key.decrypt(ast.literal_eval(str(newmsg[i]))))
  i=i+1
 return decrypted


host=sys.argv[1]
port=int(sys.argv[2])
tcp=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((host, port))

serverKey=str(tcp.recv(5000))
serverKey=serverKey.replace("\\n","\n")
serverKey=RSA.importKey(str(serverKey))

def encrypt(msg):
 encr=""
 i=0
 while(i<len(msg)/sizekey and len(msg)>sizekey):
  block=msg[i*sizekey:i*sizekey+sizekey:]
  encr=encr+str(serverKey.encrypt(block,sizekey))+spacer
  i=i+1
 block=msg[i*sizekey::]
 encr=encr+str(serverKey.encrypt(block,sizekey))
 return str(encr)

nick=sys.argv[3]

tcp.send(encrypt(publicascii))
if(tcp.recv(1)=="1"):
 tcp.send(encrypt(nick))
else:
 print "Failed!"
 quit()

#print bcolors.OKGREEN+"You are connected!"+bcolors.ENDC
def receive(tcp, ui):
 while(1):
  msg=tcp.recv(10000)
  if not msg:
    print bcolors.FAIL+"The server crashes.\nCtrl+C and try again."+bcolors.ENDC
    break
  try:
    #print bcolors.OKBLUE+decrypt(msg)+bcolors.ENDC
    ui.chatbuffer_add(decrypt(msg))
  except:
    print "Error!"

def main(stdscr):
#thread to receive messages
 stdscr.clear()
 ui = ChatUI(stdscr)
 ui.chatbuffer_add("---- You are connected")
 start_new_thread(receive,(tcp,ui))
 while(1):
  msgi=ui.wait_input("["+nick+"]"+": ")
  clock=datetime.now()
  timer="["+str(clock.hour+100)[1::]+":"+str(clock.minute+100)[1::]+":"+str(clock.second+100)[1::]+"] "  
  ui.chatbuffer_add(timer+nick+": "+msgi)
  if msgi in commandlist.list:
   c, m = commandlist.sendcommand(msgi)
   if c == 1:
    tcp.send(m)
  elif msgi[-4:len(msgi)]=="/del":
   print bcolors.FAIL+bcolors.BOLD+"INPUT BUFFER IS CLEAN"+bcolors.ENDC+bcolors.ENDC
  elif not(msgi in commandlist.avoid):
   try:
    tcp.send(encrypt(msgi))
   except:
    print "Error!"
try:
 wrapper(main)
except(KeyboardInterrupt):
 print bcolors.FAIL+"Disconnected"+bcolors.ENDC
 quit()

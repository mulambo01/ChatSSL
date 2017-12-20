import socket, sys, ssl, time
from datetime import datetime
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
from thread import start_new_thread


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


KEYFILE='key.pem'
CERTFILE='crt.pem'

host=''
port=int(sys.argv[1])

context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

connect=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig=(host, port)
connect.bind(orig)
connect.listen(1)

connect.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

#max number of connetions
limit=200
con=["0"]*limit
client=["0"]*limit
nick=["0"]*limit

#function that will manage the connection called by the index
#all the connections will have a dedicated thread running this function
def receive(index):
	conn=con[index]
	nick[index]=conn.recv(50)
	Nick=nick[index]
	print client[index],Nick
	j=0
	clock=datetime.now()
	timer="["+str(clock.hour+100)[1::]+":"+str(clock.minute+100)[1::]+":"+str(clock.second+100)[1::]+"] "

	while(j<limit and con[j]!="0"):
		if(con[j]!="1" and j!=index):
			message=bcolors.FAIL+timer+"User "+Nick+" came into the room."+bcolors.ENDC
			try:
				con[j].sendall(message)
			except:
				print "ERROR"
		j=j+1
	while(1):
		msg=conn.recv(10000)
		clock=datetime.now()
		timer="["+str(clock.hour+100)[1::]+":"+str(clock.minute+100)[1::]+":"+str(clock.second+100)[1::]+"] "
		if not msg:
			print timer+"Client "+str(index)+" exits."
			conn.close()
#the value 1 indicates that the socket was in using but now is free, 0 means that the socket is virgin
			con[index]="1"
			client[index]="1"
			nick[index]="1"
			msg=bcolors.FAIL+timer+"User "+Nick+" exits."+bcolors.ENDC
			j=0
			while(j<limit and con[j]!="0"):
				if(con[j]!="1" and j!=index):
					try:
						con[j].sendall(msg)
					except:
						print "ERROR"
				j=j+1
			break
#if the message is /who, all the users in the room will be listed
		if(msg=="/who"):
			j=0
			output=bcolors.OKGREEN+"Users: "
			while(nick[j]!="0"):
				if(nick[j]=="1"):
					continue
				else:
					output=output+"\n"+nick[j]
				j=j+1		
			try:
				con[index].sendall(output+bcolors.ENDC)
			except:
				print "ERROR /who"
		else:
			msg=timer+Nick+": "+msg
			print msg, index
			j=0
			while(j<limit and con[j]!="0"):
				if(con[j]!="1" and j!=index):
					try:
						con[j].sendall(msg)
					except:
						print "ERROR"
				j=j+1
def main():
	i=0
#this variable will be used to save cpu
	cpusave=0
	while(1):
		if(con[i]=="0" or con[i]=="1"):
			con[i], client[i]=connect.accept()
			try:
				con[i]=context.wrap_socket(con[i], server_side=True)
			except:
				print "SSL ERROR"
				error=bcolors.BOLD+bcolors.FAIL+"Problem with the SSL connection. Check if you have the SSL certificate"+bcolors.ENDC+bcolors.ENDC
				con[i].sendall(error)
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
	connect.shutdown(socket.SHUT_RDWR)
	connect.close()
	quit()

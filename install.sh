#!/bin/bash
chmod +x client.py server.py

mkdir keys
echo -n "Do you want to generate the server keys? [Y/n] "
read ANS
if [ "$ANS" != "N" -o "$ANS" != "n" ]
then
openssl genrsa -out keys/key.pem && yes '' | openssl req -new -x509 -key keys/key.pem -out keys/crt.pem
fi

if [ "$(whoami)" != "root" ]
then
echo -e "\nYou need to be root to finish the installation!"
exit 1
fi
ln -sf $PWD/server.py /usr/bin/chatsslserver
ln -sf $PWD/client.py /usr/bin/chatssl
echo -e "Creating a systemd service file:\n/etc/systemd/system/chatSSL.service"
#default port
PORT="7000"
echo -e "[Unit]\nDescription=ChatSSL server\n[Service]\nType=simple\nExecStart=/usr/bin/python2 $PWD/server.py $PORT\nExecReload=/bin/kill -HUP \$MAINPID\n[Install]\nWantedBy=multi-user.target" > $PWD/chatSSL.service
ln -sf $PWD/chatSSL.service /etc/systemd/system/chatSSL.service
echo "Success"

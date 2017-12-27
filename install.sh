#!/bin/bash
chmod +x client.py server.py
ln -sf $PWD/server.py /usr/bin/chatssl
ln -sf $PWD/client.py /usr/bin/chatsslserver
mkdir keys
echo -n "Do you want to generate the server keys? [Y/n] "
read ANS
if [ "$ANS" != "N" -o "$ANS" != "n" ]
then
openssl genrsa -out key.pem && yes '' | openssl req -new -x509 -key key.pem -out crt.pem
fi
echo -e "Creating a systemd service file:\n/etc/systemd/system/chatSSL.service"
#default port
PORT="7000"
echo -e "[Unit]\nDescription=ChatSSL server\n[Service]\nType=simple\nExecStart=/usr/bin/python2 $PWD/server.py $PORT\nExecReload=/bin/kill -HUP \$MAINPID\n[Install]\nWantedBy=multi-user.target" > $PWD1/chatSSL.service
ln -sf $PWD/chatSSL.service /etc/systemd/system/chatSSL.service
echo "Success"
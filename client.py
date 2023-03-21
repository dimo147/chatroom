import socket
import select
import sys
import os

HOST = '127.0.1.1'
PORT = 1470

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST, PORT))

nickname = input("chose a nickname: ")

while True:
    sockets_list = [sys.stdin, server]

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
 
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048).decode('utf-8')
            if message == 'NICK':
                server.send(nickname.encode('utf-8'))
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                print (message)
        else:
            message = input('')
            server.send(message.encode("utf-8"))
            print("\033[A{}\033[A".format(' '*len(message)))

server.close()

import os
import socket
from _thread import *

HOST = '127.0.1.1'
PORT = 1470

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))

server.listen(100)
os.system('cls' if os.name == 'nt' else 'clear')
print("listening...")

list_of_clients = []
nicknames = []
 
def clientthread(conn, addr):
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                index = list_of_clients.index(conn)
                nickname = nicknames[index]
                message_to_send = f"<{nickname}> {message}"
                print (message_to_send)
                broadcast(message_to_send)
            else:
                remove(conn)
        except:
            continue
 
def broadcast(message):
    for clients in list_of_clients:
        try:
            clients.send(message.encode('utf-8'))
        except:
            clients.close()
            remove(clients)
 
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
 
while True:
    conn, addr = server.accept()
    
    conn.send(b"NICK")
    nickname = conn.recv(1024).decode("utf-8")
    nicknames.append(nickname)
    list_of_clients.append(conn)
    broadcast(f"{nickname} join the chat!")
    print (addr[0] + " connected")
    start_new_thread(clientthread,(conn, addr))    
 
conn.close()
server.close()
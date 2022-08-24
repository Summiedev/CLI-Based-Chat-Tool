import socket
from _thread import *

import threading
import select
from util_main import Client
from room_user import Room,User
HEADER_LENGTH = 10
BUFFER= 4096
serverIP = "127.0.0.1"
#serverIP = "0.0.0.0"
serverPORT = 1234
MAX_CLIENTS=15
def create_server(addr):
    new_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    new_server_socket.setblocking(0)
    new_server_socket.bind(addr)
    new_server_socket.listen(MAX_CLIENTS)
    print(f'Connected to {addr} hsahahahsa')
    return new_server_socket
client = Client()
server_socket = create_server((serverIP,serverPORT)) 


sockets_list = [server_socket]

clients = {}

def accept_connect():
    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                new_user = User(client_socket)
                sockets_list.append(new_user)
                client.welcome_new(new_user)
            else:
                message = notified_socket.socket.recv(BUFFER)
                if message:
                    client.input_actions(notified_socket, message.decode())

                else:
                    
                    notified_socket.socket.close()
                    sockets_list.remove(notified_socket)

                
        for notified_socket in exception_sockets:

            sockets_list.remove(notified_socket)
#while True:
start_new_thread(accept_connect())

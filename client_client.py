import socket
import select
import errno
import threading
import sys
from itertools import count
from logo import  WELCOME_BANNER
HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
BUFFER= 4096



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    x = count(100)
    try:
       client_socket.connect((IP, PORT))
       print("Succesfuly Connected to the Server") 
       print(WELCOME_BANNER)
       welcome_msg = client_socket.recv(BUFFER)
       print(welcome_msg.decode())
    except:
        print(f'Unable to connect to the Server at {IP}{PORT}')
    username = input("Username: ")
    if username !='':
        client_socket.sendall(('name: '+username).encode())
        instruction_msg = client_socket.recv(BUFFER)
        print(instruction_msg.decode())
    else:
        val = str(next(x))
        username ="Client"+val
        client_socket.sendall(('name: '+username).encode())
        instruction_msg = client_socket.recv(BUFFER)        
        print("Invalid Username, username cannot be empty! But don't worry, your username is "+username)
        print(instruction_msg.decode())
    while True:
        send_msg(username)
        threading.Thread(target=listen_msgs,args=(client_socket, )).start()
def send_msg(name):
    #message = input(f'{name}:>:>:>:>: ')
    message = input()
    print("\033[A"+'\033[K'+"\033[A")
        
    if message != '':
        client_socket.sendall(message.encode())
        #print("Sent")
    else:
        print("Empty Message, Message cannot be empty, please type something")
def listen_msgs(client):
    while True:
        msgs = client.recv(BUFFER).decode()
       
        if msgs !='':
            print(msgs)
        else:
            sys.exit()
connect()

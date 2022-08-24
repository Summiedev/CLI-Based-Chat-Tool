import select,socket
import datetime
class Room:
    def __init__(self, name):
        self.name= name
        self.occupants_name=[]
        self.occupants =[]
        self.room ={}
    def get_name(self):
        return self.name
    def welcome_new(self,from_user):
        #New user
        msg = "\nChatroom[" +self.name + "] welcomes a new user named " + from_user.name + ' to the chat\n'
        print(msg)
        for user in self.occupants:
          if user.name!= from_user.name:
            user.socket.send(msg.encode())
    def join_room(self, user):
        self.occupants_name.append(user.name)
        self.occupants.append(user)
    def save_text(self,from_user,message):
        msg_list =[]
        e = datetime.datetime.now()
        
        time_name = f'{e.day}-{e.month}-{e.year}-{e.hour}-{e.minute}-{e.second}'
        message_chat = f'[{from_user.name}] :>:>:>: {message}'
        msg_list.append(message_chat)
        with open(f'Chats{time_name}.txt', 'w') as f:
            for line in msg_list:
                f.write(line)
                f.write('\n')
    
    def send_msg(self,from_user,message):
        
        message = f'[{from_user.name}] :>:>:>: {message}'
        
        for user in self.occupants:
            user.socket.sendall(message.encode())    
    def switch_name(self,user,message_new):
        old_name = user.name
        if user in self.occupants:
            user.name = message_new
    def send_name(self,old,message_new):
        message = f'[{old}] has changed their name to {message_new}'
        for user in self.occupants:
            user.socket.sendall(message.encode())
    def remove_client(self, user):
        self.occupants_name.remove(user.name)
        if user in self.occupants:
            self.occupants.remove(user)
        msg = user.name + "has either disconnected or ledft the room"
        user.socket.sendall(msg.encode())
    
        
class User:
    def __init__(self, socket, name="new"):
        socket.setblocking(0)
        self.name =name
        self.socket= socket
        self.chat_msg ={}
    def fileno(self):
        return self.socket.fileno()
        
import select,socket,sys,time
import datetime
from manual import manual_s,wrong_commmand
from room_user import Room,User
from itertools import count
serverPort = 3000
MAX_CLIENTS = 20

class Client:
    def __init__(self):
        self.chats={}
        self.rooms_name ={}
        self.room_user_map={}
        
        self.x = count(1)
    def welcome_new(self, new_user):
        new_user.socket.sendall('Welcome to DSJK ChatRoom! Please enter your username below to continue.\n'.encode())
    
    def input_actions(self, user,message):
        print(f'{user.name} is using a command or sending a Message which says {message}')
        command = message.split()[0]
        if "name:" in message:
            name = message.split()[1]
            if name not in self.room_user_map.keys():
                user.name = name
                print(f'{user.name} just joined')
                user.socket.sendall(manual_s(user.name).encode())
            else:
                val = str(next(self.x))
                user.name = "Client"+val
                print(f'{user.name} just joined')
                rep = f'Your username has been set to {user.name} because initial name exists.'
                user.socket.sendall((rep+manual_s(user.name)).encode())
        elif command =="<join>":
            self.join_room(user,message)
        elif command =="<list>":
            self.list_names_room(user)
        elif command =="<create>":
            self.create_room(user,message)
        elif command =="<create_pvt>":
            self.create_pvt_room(user,message)
        elif command =="<change_nme>":
            self.change_username_room(user,message)
        elif command =="<help>":
            self.help_room(user)
        elif command =="<leave>":
            self.leave_room(user,message)
        elif command =="<quit>":
            self.quit_server(user)
        elif command =="switch":
            self.switch_room(user,message)
        # elif command =="save":
        #     self.save_history_room(user,message)
        else:
           #msg_list=[]
           same_chat = True
           if user.name in self.room_user_map:
                #user.socket.sendall(message.encode())
                self.rooms_name[self.room_user_map[user.name]].send_msg(user, message)
                old_room = self.room_user_map[user.name]
                
           else:
                print("No Room Discovered")
                x = f'''You are Currently not in any room so you can not send any message yet!
Use [<list>]\t\t Display list of existing chatrooms.
Use [<join> room_name]\t Join an existing chatroom.
Use [<create> room_name]\t Create a new chatroom.
Use [<create_pvt> room_name] Create a new private chatroom.
Use [<quit>]\t\t Quit the server '''
                user.socket.send(x.encode())
    
    def join_room(self,user, message):
        if len(message.split()) ==2:
            room_name = message.split()[1]
            if user.name in self.room_user_map.keys():
                rep = f'Currently you are at f{room_name}, Try another command'
                user.socket.sendall(rep.encode())
            else:
                if room_name in self.rooms_name:
                    user.socket.send(f"\nYou joined a chatroom named {room_name}".encode())
                    self.rooms_name[room_name].welcome_new(user)
                    #self.rooms[room_name].users.append(user)
                    self.rooms_name[room_name].join_room(user)
                    self.room_user_map[user.name] =room_name
                    print(self.room_user_map)
                    
                else:
                    message = "\nRooms is unavailable, create one or check list for available rooms"
                    user.socket.sendall(message.encode())
                    
        else:
            user.socket.sendall(wrong_commmand(user.name).encode()) 
    def create_room(self,user, message):
        if len(message.split())==2:
            room_name = message.split()[1]
            if user.name in self.room_user_map.keys():
                rep = "\nYour username is already in a room,Please leave the room to create another room"
                user.socket.sendall(rep.encode())
            elif room_name in self.room_user_map.values():
                rep = "\nRoom Name exists, please use another name"
                user.socket.sendall(rep.encode())
            else:
                 new_room = Room(room_name)
                 self.rooms_name[room_name]= new_room
                 user.socket.send(f"You created a chatroom named {room_name}".encode())
                 self.rooms_name[room_name].welcome_new(user)
                 self.rooms_name[room_name].join_room(user)
                 self.room_user_map[user.name] =room_name
                 print(self.room_user_map)
                 
        else:  
            user.socket.sendall((wrong_commmand(user.name)).encode())
    def list_names_room(self,user):
        if(len(self.rooms_name)) == 0:
            rep = "\nNo rooms available currently. Please wait till other users create rooms or\nUse [create] room_name to create a room or <create_pvt> room_name to create a private room"
            print((rep))
            user.socket.sendall(rep.encode())
        else:
            count=0
            rep ="\nList of existing current public rooms....\n"
            public_list = [x for x in self.rooms_name if x.startswith("<pvt>") is False]
            #for room in self.rooms_name:
            for room in public_list:
                
                
                occ = [x.name for x in  self.rooms_name[room].occupants]
                occ = ",".join(occ)
                count+=1
                rep+= str(count) +".) Chatroom[" + room + "] has " + str(len(self.rooms_name[room].occupants)) +" occupant(s) namely "+ occ + ".\n"
            user.socket.sendall(rep.encode())
    def create_pvt_room(self,user, message):
        if len(message.split())==2:
            room_nme = message.split()[1]
            room_name ="<pvt>"+room_nme
            
            if user.name in self.room_user_map.keys():
                rep = "\nYour usernname is already in a room,Please leave the room to create another room"
                user.socket.send(rep.encode())
            elif room_name in self.room_user_map.values():
                rep = "\nPrivate room Name exists, please use another name"
                user.socket.send(rep.encode())
            else:
                 new_room = Room(room_name)
                 self.rooms_name[room_name]= new_room
                 user.socket.send(f"You created a Private chatroom named {room_nme}".encode())
                 self.rooms_name[room_name].welcome_new(user)
                 self.rooms_name[room_name].join_room(user)
                 self.room_user_map[user.name] =room_name
                 print(self.room_user_map)
                 
        else:  
            user.socket.sendall((wrong_commmand(user.name)).encode())
    def change_username_room(self,user, message):
        user_new_name = message.split()[1]
        same_name = False
        if user_new_name in self.room_user_map:
            rep = "\nThat username exists, please try another name"
            same_name = True
            user.socket.send(rep.encode())
        elif user.name not in self.room_user_map:
            same_name = True
            rep = "You have to be in a room to be able to change your username "
            user.socket.send(rep.encode())
        else:
            old_name = user.name
            old_room = self.room_user_map[user.name]
            self.room_user_map[user_new_name] = self.room_user_map[old_name]
            del self.room_user_map[old_name]
            self.rooms_name[old_room].switch_name(user,user_new_name)
           
            self.rooms_name[old_room].send_name(old_name,user_new_name)
           
            print((self.room_user_map))
    def help_room(self,user):
        user.socket.sendall((manual_s(user.name)).encode())
    def remove_users(self, user):
        left_room =self.room_user_map[user.name]
        self.room_user_map.pop(user.name,None)
        self.rooms_name[left_room].remove_client(user)
    def leave_room(self,user,message):
        if user.name not in self.room_user_map.keys():
            user.socket.send("\nYou're not currently in any room,Join a room first before you can leave".encode())
        else:
            print("Saving message.................")
            # e = datetime.datetime.now()    
            # time_name = f'{e.day}-{e.month}-{e.year}-{e.hour}-{e.minute}-{e.second}'
            # with open(f'Chats{time_name}.txt', 'w') as f:
            #     for line in self.msg_list:
            #         f.write(line)
            #         f.write('\n')
            # time.sleep(3)
            # print("Message Saved")
            self.remove_users(user)
            
            msg =f'{user.name} left the chat'
            
            print(msg+str(self.room_user_map))
    
    def quit_server(self,user):
        if user.name not in self.room_user_map.keys():
            msg =user.name+"is quitting the server"
            print(msg)
           
            user.socket.close()
        else:
            self.remove_users(user)
            msg =user.name+"is quitting the server"
            user.socket.close()
           
            
    def switch_room(self,user, message):
        same_room = False
        if len(message.split())==2:
            room_name = message.split()[1]
            
            if user.name in self.room_user_map.keys():
                if self.room_user_map[user.name] == room_name:
                    same_room = True
                    rep = "Your are already in ["+room_name+"] room,Please leave the room or create another room"
                    user.socket.send(rep.encode())
                else:
                    old_room = self.room_user_map[user.name]
                    self.rooms_name[old_room].remove_client(user)
            else:
                rep = "\nNo rooms available currently. Please wait till other users create rooms or\nUse [create] room_name to create a room or <create_pvt> room_name to create a private room"
                print((rep))
                user.socket.sendall(rep.encode())
                same_room = True
            if same_room == False:
                 new_room = Room(room_name)
                 self.rooms_name[room_name]= new_room
                 user.socket.send(f"You created a Private chatroom named {room_name}".encode())
                 self.rooms_name[room_name].welcome_new(user)
                 self.rooms_name[room_name].join_room(user)
                 self.room_user_map[user.name] =room_name
                 print(self.room_user_map)
                 
        else:  
            user.socket.sendall((wrong_commmand(user.name)).encode())
   
                
        
                
            
            
            
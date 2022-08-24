
def manual_s(username):
    
    manual =f'''\nWelcome {username}, here are the lists of commands to proceed
[<list>]\t\t Display list of existing chatrooms.
[<join> room_name]\t Join an existing chatroom.
[<create> room_name]\t Create a new chatroom.
[<create_pvt> room_name] Create a new private chatroom.
[<switch> room_name]\t Switch to another chatroom.
[<change_nme> name>] Change Current Username.
[<save>]\t\t Save current chat history.
[<help>]\t\t Provides Help information for commands.
[<leave>]\t\t Leave current chatroom.
[<quit>]\t\t Quit the server\n
Please Enter your Command Below.'''
    return manual
def wrong_commmand(username):
    alertcommm = f'''\nHey {username}! That's not the right way to use it! Check below:
[<list>]\t\t Display list of existing chatrooms.
[<join> room_name]\t Join an existing chatroom.
[<create> room_name]\t Create a new chatroom.
[<create_pvt> room_name] Create a new private chatroom.
[<switch> room_name]\t Switch to another chatroom.
[<change_nme> name>] Change Current Username.
[<save>]\t\t Save current chat history.
[<help>]\t\t Provides Help information for commands.
[<leave>]\t\t Leave current chatroom.
[<quit>]\t\t Quit the server\n
Please Enter your Command Below.'''
    return alertcommm

        

import grpc
import sys
import threading
import os
import chatRPC_pb2
import chatRPC_pb2_grpc

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 2d672b5 (Switch to new client)
def register_account(stub, username, password):
    register_response = stub.RegisterUser(chatRPC_pb2.RegisterRequest(username=username, password=password))
    if not register_response.status:
        print('That username already exists. Please enter a different username.')
        return False
    return True
<<<<<<< HEAD

def login(stub, username, password):
    login_response = stub.Login(chatRPC_pb2.LoginRequest(username=username, password=password))
    if not login_response.status:
        print('Your username or password is incorrect. Please try again.')
        return None

    auth_token = login_reponse.text
    with open('auth.crt', 'rw') as cert:
        cert.write(auth_token + '\n')
    
    return auth_token
=======
def message_stream(stub):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
>>>>>>> 7ca4f33 (First attempt at kafka integration)

def user_pass_prompt():
    print('Please enter your desired username:')
    username = input()
    print('Please enter your desired password:')
    password = input()
    return username, password

=======

def login(stub, username, password):
    login_response = stub.Login(chatRPC_pb2.LoginRequest(username=username, password=password))
    if not login_response.status:
        print('Your username or password is incorrect. Please try again.')
        return None

    auth_token = login_reponse.text
    with open('auth.crt', 'rw') as cert:
        cert.write(auth_token + '\n')
    
    return auth_token

def user_pass_prompt():
    print('Please enter your desired username:')
    username = input()
    print('Please enter your desired password:')
    password = input()
    return username, password

>>>>>>> 2d672b5 (Switch to new client)
def direct_message(stub, params, token):
    try:
        recipient = params[1]
        message = ' '.join([str(x) for x in params[2]])
    except:
        print('You are missing information in your direct message. Please use dm [username] [message].')
        return

    dm_response = stub.DirectMessage(chatRPC_pb2.DirectMessageRequest(recipient=recipient, message=message, access_token=token))
    if not dm_response.status:
        print(dm_response.text)

def channel_post(stub, params, token):
    try:
        channel = params[1]
        message = ' '.join([str(x) for x in params[2]])
    except:
        print('You are missing information in your channel post. Please use post [channel] [message].')
        return

    post_response = stub.ChannelPost(chatRPC_pb2.ChannelPostRequest(channel_name=channel, message=message, access_token=token))
    if not post_response.status:
        print(post_response.text)

def watch_channel(stub, params, token):
    try:
        channel = params[1]
    except:
        print('You are missing information in your channel watch. Please use watch [channel].')
        return

    watch_response = stub.Watch(chatRPC_pb2.WatchRequest(channel_name=channel, access_token=token))
    if not watch_response.status:
        print(watch_response.text)
    else:
        print('Watching channel: ' + channel)

def unwatch_channel(stub, params, token):
    try:
        channel = params[1]
    except:
        print('You are missing information in your channel unwatch. Please use unwatch [channel].')
        return

    watch_response = stub.Unwatch(chatRPC_pb2.UnwatchRequest(channel_name=channel, access_token=token))
    if not watch_response.status:
        print(watch_response.text)
    else:
        print('No longer watching channel: ' + channel)

def block_user(stub, params, token):
    try:
        username = params[1]
    except:
        print('You are missing information in your block. Please use block [username].')
        return

    block_response = stub.Block(chatRPC_pb2.BlockRequest(blocked_user=username, access_token=token))
    if not block_response.status:
        print(block_response.text)
    else:
        print('Blocked user: ' + channel)

def unblock_user(stub, params, token):
    try:
        username = params[1]
    except:
        print('You are missing information in your unblock. Please use unblock [username].')
        return

    unblock_response = stub.Unblock(chatRPC_pb2.UnblockRequest(blocked_user=username, access_token=token))
    if not unblock_response.status:
        print(unblock_response.text)
    else:
        print('Unblocked user: ' + channel)

def get_help():
    print('''
        You can take the following actions:\n
        dm [username] [message] - to direct message a user\n
        post [channel] [message] - to post to a channel\n
        watch [channel] - to begin watching a channel\n
        unwatch [channel] - to stop watching a channel\n
        block [username] - to block a user\n
        unblock [username] - to unblock a blocked user\n
        -----------------------------------------------\n
        The following channels are available to you:\n
        ...
        ''')

def check_auth(stub):
    if os.path.exists('auth.crt')
        with open('auth.crt', 'r') as cert:
            auth_token = cert.readline().strip()
            check_login = stub.ChannelPost(chatRPC_pb2.ChannelPostRequest(channel_name='test', message='test', access_token=auth_token))
            if check_login.text != 'Unauthenticated.':
                return auth_token
    return None

def incoming_message_stream(stub):
    for response in stub.MessageStream(chatRPC_pb2.Empty()):
        print(response.text)

def user_requests(stub):
<<<<<<< HEAD
<<<<<<< HEAD
    auth_token = check_auth(stub)

    while(True):
        first_loop = True
        if auth_token == None:
=======

    authorized = False
    
    if os.path.exists("auth.txt"):
        
        key_file = open("auth.txt","r")

        username = key_file.readline().strip()
        key = key_file.readline().strip()

        # test = stub.ChannelPost(chatRPC_pb2.ChannelPostRequest(username = username, channel_name = "test", message = "", key = key))

        # if test.text != "Unauthenticated.":
            
        #     authorized = True

    first_loop = True

    while(True):

        if authorized is False:
            
>>>>>>> 7ca4f33 (First attempt at kafka integration)
=======
    auth_token = check_auth(stub)

    while(True):
        first_loop = True
        if auth_token == None:
>>>>>>> 2d672b5 (Switch to new client)
            print('Welcome to the chat application.')
            print('Would you like to register a new account? Type yes, or no.')
            register_account = input().lower().strip()

            if register_account not in ['yes', 'no']:
                print('Please enter yes or no.')
                continue

            if register_account == 'yes':
                successful_register = False
                while not successful_register:
                    username, password = user_pass_prompt()
                    successful_register = register_account(stub, username, password)
                login(stub, username, password)

            while auth_token == None:
                username, password = user_pass_prompt()
                auth_token = login(stub, username, password)

        if first_loop:
            print('Enter help for available actions and channels.')
            first_loop = False
        
<<<<<<< HEAD
<<<<<<< HEAD
        action = input().strip().split()
        if len(action) == 0:
=======
        action = input().strip().split(' ')
        
        if not action:
            continue


        if action[0].lower().strip() == 'help':
            
            print('''
            You can take the following actions:\n
            dm [username] [message] - to direct message a user\n
            post [channel] [message] - to post to a channel\n
            watch [channel] - to begin watching a channel\n
            unwatch [channel] - to stop watching a channel\n
            block [username] - to block a user\n
            unblock [username] - to unblock a blocked user\n
            -----------------------------------------------\n
            The following channels are available to you:\n
            ...
            ''')
>>>>>>> 7ca4f33 (First attempt at kafka integration)
=======
        action = input().strip().split()
        if len(action) == 0:
>>>>>>> 2d672b5 (Switch to new client)
            continue
        
        action[0] = action[0].lower()        
        if action[0] not in ['dm', 'post', 'watch', 'unwatch', 'block', 'unblock', 'help']:
            print("That is not a valid action, please retry or say 'help' for more info.")
            continue

<<<<<<< HEAD
<<<<<<< HEAD
=======
        elif len(action) < 2 and action[0] in  ["watch", "unwatch", "block", "unblock"]:
            print("You are missing information in your action.")
            continue

        elif len(action) < 3 and action[0] in ["dm","post"]:
            print("You are missing information in your action.")
            continue

        else:

            i = 1
            while action[i] == "":
                del action[i]
            
            if action[0] in ["dm", "post"]:

                i =  2
                while action[i] == "":
                    del action[i]

>>>>>>> 7ca4f33 (First attempt at kafka integration)
        if action[0] == 'dm':
            direct_message(stub, action, auth_token)
        elif action[0] == 'post':
<<<<<<< HEAD
            channel_post(stub, action, auth_token)
        elif action[0] == 'watch':
            watch_channel(stub, action, auth_token)
=======

            try:

                channel = action[1]
                message = ""
                for word in action[2:]: message = message + " " + word

            except IndexError:

                print('You are missing information in your action.')
                continue

            post_response = stub.ChannelPost(chatRPC_pb2.ChannelPostRequest(channel_name = channel, message = message, access_token = key))

            if post_response.status == False:

                print(post_response.text)

        elif action[0] == 'watch':

            try:

                channel = action[1]
            
            except IndexError:

                print('You are missing information in your action.')
                continue

            watch_response = stub.Watch(chatRPC_pb2.WatchRequest(channel_name = channel, access_token = key))

            if watch_response.status == False:
                print(watch_response.text)

            else:

                print('watching channel: ' + channel)
        
>>>>>>> 7ca4f33 (First attempt at kafka integration)
=======
        if action[0] == 'dm':
            direct_message(stub, action, auth_token)
        elif action[0] == 'post':
            channel_post(stub, action, auth_token)
        elif action[0] == 'watch':
            watch_channel(stub, action, auth_token)
>>>>>>> 2d672b5 (Switch to new client)
        elif action[0] == 'unwatch':
            unwatch_channel(stub, action, auth_token)        
        elif action[0] == 'block':
            block_user(stub, action, auth_token)        
        elif action[0] == 'unblock':
            unblock_user(stub, action, auth_token)
        else:
            get_help()

def run():
<<<<<<< HEAD
<<<<<<< HEAD
    with grpc.insecure_channel('localhost:3001') as channel:
=======
    
    port_number = '3001'

    with grpc.insecure_channel('localhost:' + port_number) as channel:

>>>>>>> 7ca4f33 (First attempt at kafka integration)
=======
    with grpc.insecure_channel('localhost:3001') as channel:
>>>>>>> 2d672b5 (Switch to new client)
        stub = chatRPC_pb2_grpc.ChatServiceStub(channel)
        threading.Thread(target=incoming_message_stream, args=(stub), daemon=True).start()
        user_requests(stub)

run()
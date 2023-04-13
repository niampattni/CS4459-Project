
import grpc
import sys
import threading
import os
import chatRPC_pb2
import chatRPC_pb2_grpc

def register_account(stub, username, password):
    register_response = stub.RegisterUser(chatRPC_pb2.RegisterRequest(username=username, password=password))
    if not register_response.status:
        print('That username already exists. Please enter a different username.')
        return False
    return True

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
    auth_token = check_auth(stub)

    while(True):
        first_loop = True
        if auth_token == None:
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
        
        action = input().strip().split()
        if len(action) == 0:
            continue
        
        action[0] = action[0].lower()        
        if action[0] not in ['dm', 'post', 'watch', 'unwatch', 'block', 'unblock', 'help']:
            print("That is not a valid action, please retry or say 'help' for more info.")
            continue

        if action[0] == 'dm':
            direct_message(stub, action, auth_token)
        elif action[0] == 'post':
            channel_post(stub, action, auth_token)
        elif action[0] == 'watch':
            watch_channel(stub, action, auth_token)
        elif action[0] == 'unwatch':
            unwatch_channel(stub, action, auth_token)        
        elif action[0] == 'block':
            block_user(stub, action, auth_token)        
        elif action[0] == 'unblock':
            unblock_user(stub, action, auth_token)
        else:
            get_help()

def run():
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = chatRPC_pb2_grpc.ChatServiceStub(channel)
        threading.Thread(target=incoming_message_stream, args=(stub), daemon=True).start()
        user_requests(stub)

run()
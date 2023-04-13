
import grpc
import sys
import threading
import os

import chatRPC_pb2
import chatRPC_pb2_grpc



 def message_stream(stub):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """

        for response in stub.MessageStream(chatRPC_pb2.Empty()):  # this line will wait for new messages from the server!

            print(response.text)

def user_requests(stub):

    authorized = False
    
    if os.path.exists("auth.txt"):
        
        key_file = open("auth.txt","r")

        username = key_file.readline().strip()
        key = key_file.readline().strip()

        test = stub.ChannelPost(chatRPC_pb2.ChannelPostRequest(username = username, channel_name = "test", message = "", key = key))

        if test.text != "Unauthenticated.":
            
            authorized = True


    while(True):

        first_loop = True

        if authorized is False:
            
            print('Welcome to the chat application.')

            print('Would you like to register a new account? Type yes, or no.')
            
            register_account = input().lower().strip()

            if register_account not in ['yes', 'no']:

                print('Please enter yes, or no.')

                continue


            if register_account == 'yes':

                print('Please enter your desired username:')
                username = input()
                print('Please enter your desired password:')
                password = input()

                register_response = stub.RegisterUser(chatRPC_pb2.RegisterRequest(username = username, password = password))

                if register_response.status == False:

                    print('That username already exists. Please enter a different username.')
                    continue
                
                else:

                    print('Logging in to your new account!')
                    
                    login_response = stub.Login(chatRPC_pb2.LoginRequest(username = username, password = password))

                    if login_response.status is False:
                        
                        print('Your username or password is incorrect. Please try again.')
                        continue
                    
                    elif login_response.status is True:

                        key = login_response.text
                        key_file = open("auth.txt","w")

                        key_file.write(username + "\n")
                        key_file.write(key + "\n")

                        authorized = True
                        print("You are logged in!")

            elif register_account == 'no':

                print('Please enter your username:')
                username = input()
                print('Please enter your password:')
                password = input()

                login_response = stub.Login(chatRPC_pb2.LoginRequest(username = username, password = password))

                if login_response.status is False:
                    
                    print('Your username or password is incorrect. Please try again.')
                    continue
                
                elif login_response.status is True:

                    key = login_response.text
                    key_file = open("auth.txt","w")

                    key_file.write(username + "\n")
                    key_file.write(key + "\n")

                    authorized = True
                    print("You are logged in!")

        if first_loop is True:

            print('enter help for available actions, and channels')
            
            first_loop = False
        
        action = input().strip()
        
        if action == '':
            continue


        if action.lower().strip() == 'help':
            
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
            continue
        
        action[0] = action[0].lower()

        if action[0] not in ['dm', 'post', 'watch','unwatch','block','unblock']:
            print("that is not a valid action")
            continue

        elif len(action) < 2 and action[0] in  ["watch", "unwatch", "block", "unblock"]:
            print("You are missing information in your action.")
            continue

        elif len(action < 3) and action[0] in ["dm","post"]:
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

        if action[0] == 'dm':

            try:

                recipient = action[1]

                message = ""
                for word in action[2:]: message = message + " " + word

            
            except IndexError:

                print('You are missing information in your action.')
                continue

            dm_response = stub.DirectMessage(chatRPC_pb2.DirectMessageRequest(sender = username, recipient = recipient, message = message, key = key))

            if dm_response.status == False:
                print(dm_response.text)
            else:
                print('Messaged ' + recipient + ': ' + message)
        
        elif action[0] == 'post':

            try:

                channel = action[1]
                message = ""
                for word in action[2:]: message = message + " " + word

            except IndexError:

                print('You are missing information in your action.')
                continue

            post_response = stub.ChannelPost(chatRPC_pb2.ChannelPostRequest(username = username, channel_name = channel, message = message, key = key))

            if post_response.status == False:

                print(post_response.text)

        elif action[0] == 'watch':

            try:

                channel = action[1]
            
            except IndexError:

                print('You are missing information in your action.')
                continue

            watch_response = stub.Watch(chatRPC_pb2.WatchRequest(username = username, channel_name = channel, key = key))

            if watch_response.status == False:
                print(watch_response.text)

            else:

                print('watching channel: ' + channel)
        
        elif action[0] == 'unwatch':

            try:

                channel = action[1]
            
            except IndexError:

                print('You are missing information in your action.')
                continue
                
            unwatch_response = stub.Unwatch(chatRPC_pb2.UnwatchRequest(username = username, channel_name = channel, key = key))

            if unwatch_response.status == False:
                print(unwatch_response.text)
            
            else:
                print('unwatched channel: ' + channel)
        
        elif action[0] == 'block':

            try:

                blocked_user = action[1]
            
            except IndexError:

                print('You are missing information in your action.')
                continue

            block_response = stub.Block(chatRPC_pb2.BlockRequest(username = username, blocked_user = blocked_user, key = key))

            if block_response.status == False:
                print(block_response.text)
            
            else:
                print('Blocked User: ' + blocked_user)
        
        elif action[0] == 'unblock':

            try:

                blocked_user = action[1]
            
            except IndexError:

                print('You are missing information in your action.')
                continue

            unblock_response = stub.Unblock(chatRPC_pb2.UnblockRequest(username = username, blocked_user = blocked_user, key = key))

            if unblock_response.status == False:
                print(unblock_response.text)
            
            else:
                print('Unblocked User: ' + blocked_user)

def run():
    
    port_number = '63718'

    with grpc.insecure_channel('localhost:' + port_number) as channel:

        stub = chatRPC_pb2_grpc.ChatServiceStub(channel)

        threading.Thread(target=message_stream, args=(stub), daemon=True).start()

        user_requests(stub)

run()
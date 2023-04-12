
import grpc
import sys

import chatRPC_pb2
import chatRPC_pb2_grpc

key = None
username = ""

port_number = "4000"
register_account = ""
first_loop = True

def run():

    with grpc.insecure_channel('localhost:' + port_number) as channel:

        stub = ops_pb2_grpc.chatServiceStub(channel)


        while(True):

            if Key is None:
                
                print("Welcome to the chat application.")

                print("Would you like to register a new account? Type yes, or no.")
                
                register_account = input().lower()

                if register_account not in ["yes", "no"]:

                    print("Please enter yes, or no.")

                    continue


                if register_account == "yes":

                    print("Please enter your desired username:")
                    username = input()
                    print("Please enter your desired password:")
                    password = input()

                    register_response = stub.RegisterUser(chatRPC_pb2.RegisterRequest(username = username, password = password))

                    if register_response.status == False:

                        print("That username already exists. Please enter a different username.")
                        continue
                    
                    else:

                        print("Logging in to your new account!")
                        
                        login_response = stub.Login(chatRPC_pb2.LoginRequest(username = username, password = password))

                        if login_response.status is False:
                            
                            print("Your username or password is incorrect. Please try again.")
                            continue
                        
                        elif login_response.status is True:

                            key = login_response.text

                elif register_account == "no"

                    print("Please enter your username:")
                    username = input()
                    print("Please enter your password:")
                    password = input()

                    login_response = stub.Login(chatRPC_pb2.LoginRequest(username = username, password = password))

                    if login_response.status is False:
                        
                        print("Your username or password is incorrect. Please try again.")
                        continue
                    
                    elif login_response.status is True:

                        key = login_response.text

            if first_loop is True:

                print("enter 'help' for available actions, and channels")
                
                first_loop = False
            
            action = input()
            
            if action == "":
                continue


            if action.lower().strip() == "help":
                
                print("""
                You can take the following actions:\n
                DM username message - to direct message a user\n
                POST channel message - to post to a channel\n
                WATCH channel - to begin watching a channel\n
                UNWATCH channel - to stop watching a channel\n
                BLOCK username - to block a user\n
                UNBLOCK username - to unblock a blocked user\n
                -----------------------------------------------\n
                The following channels are available to you:\n
                ...
                """)
                continue

            action = action.split(" ")

            if action[0] == "DM":

                try:

                    recipient = action[1]
                    message = action[2]
                
                except IndexError:

                    print("You are missing information in your action.")
                    continue

                dm_response = stub.DirectMessage(chatRPC_pb2.DirectMessageRequest(sender = username, recipient = recipient, message = message, key = key))

                if dm_response.status == False:
                    print(dm_response.text)
                else:
                    print("Messaged " + recipient + ": " + message)
            
            elif action[0] == "POST":

                try:

                    channel = action[1]
                    message = action[2]

                except IndexError:

                    print("You are missing information in your action.")
                    continue

                post_response = stub.ChannelPost(chatRPC_pb2.ChannelPostRequest(username = username, channel_name = channel, message = message, key = key))

                if post_response.status == False:

                    print(post_response.text)

            elif action[0] == "WATCH":

                try:

                    channel = action[1]
                
                except IndexError:

                    print("You are missing information in your action.")
                    continue

                watch_response = stub.Watch(chatRPC_pb2.WatchRequest(username = username, channel_name = channel, key = key))

                if watch_response.status == False:
                    print(watch_response.text)

                else:

                    print("watching channel: " + channel)
            
            elif action[0] == "UNWATCH":

                try:

                    channel = action[1]
                
                except IndexError:

                    print("You are missing information in your action.")
                    continue
                    
                unwatch_response = stub.Unwatch(chatRPC_pb2.UnwatchRequest(username = username, channel_name = channel, key = key))

                if unwatch_response.status == False:
                    print(unwatch_response.text)
                
                else:
                    print("unwatched channel: " + channel)
            
            elif action[0] == "BLOCK":

                try:

                    blocked_user = action[1]
                
                except IndexError:

                    print("You are missing information in your action.")
                    continue

                block_response = stub.Block(chatRPC_pb2.BlockRequest(username = username, blocked_user = blocked_user, key = key))

                if block_response.status == False:
                    print(block_response.text)
                
                else:
                    print("Blocked User: " + blocked_user)
            
            elif action[0] == "UNBLOCK":

                try:

                    blocked_user = action[1]
                
                except IndexError:

                    print("You are missing information in your action.")
                    continue

                unblock_response = stub.Unblock(chatRPC_pb2.UnblockRequest(username = username, blocked_user = blocked_user, key = key))

                if unblock_response.status == False:
                    print(unblock_response.text)
                
                else:
                    print("Unblocked User: " + blocked_user)





run()
        
                
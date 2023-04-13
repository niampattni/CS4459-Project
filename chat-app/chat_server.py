
from concurrent import futures
import grpc
import chatRPC_pb2
import chatRPC_pb2_grpc
import sys
import os
import mysql.connector as db
from datetime import datetime

class ChatAppManager(chatRPC_pb2_grpc.ChatServiceServicer):

    def __init__(self):
        self.chats = []
    
    def message_receiver(self, message_sender, message_text, message_date, message_from_channel=False, message_channel_name=None):
        if message_from_channel:
            self.chats.append(chatRPC_pb2.MessageResponse(from_name=message_from, text=message_text, date=message_date, channel_name=message_channel_name))
        else:
            self.chats.append(chatRPC_pb2.MessageResponse(from_name=message_from, text=message_text, date=message_date))

    def get_db(self):
        # Open connection to DB and return cursor
        conn = db.connect(host='chat-app-db', port=3306, user='chat-app', password=os.environ.get('MYSQL_PASSWORD'), database='ChatApp')
        cur = conn.cursor()
        return conn, cur
    
    def get_missed_messages(self, user_id, cur, conn):
        # Upon login, retrieve missed messages
        data = {
            'id': user_id
        }
        query = 'SELECT message, from_user, sender_name, datetime FROM Missed WHERE user_id=%(id)s'
        cur.execute(query, data)

        # TODO: Display missed messages with Kafka

    def get_user(self, conn, cur, token):
        # Check if access token is valid
        data = {
            'token': token
        }
        query = 'SELECT user_id FROM Online WHERE access_token=%(token)s;'
        cur.execute(query, data)

        # If invalid token then return None and exit
        if cur.rowcount == 0:
            return None

        # If valid token then return User object
        row = cur.fetchone()
        data = {
            'id': row[0]
        }
        query = 'SELECT id, username FROM User WHERE id=%(id)s;'
        cur.execute()
        return cur.fetchone()

    def is_blocked(self, conn, cur, user_id, recipient_id):
        data = {
            'user_id': user_id,
            'block_id': recipient_id
        }
        query = 'SELECT * FROM Block WHERE user_id=%(user_id)s AND block_id=%(block_id)s;'
        cur.execute(query, data)

        if cur.rowcount == 0:
            data = {
                'user_id': recipient_id,
                'block_id': user_id
            }
            query = 'SELECT * FROM Block WHERE user_id=%(user_id)s AND block_id=%(block_id)s;'
            cur.execute(query, data)

        return cur.rowcount > 0
    
    def block_helper(self, request, block):
        response_message = ''
        conn, cur = self.get_db()
        # Check if logged in
        user = self.get_user(conn, cur, request.access_token)
        if user == None:
            response_message = 'Unauthenticated.'
            status = False
            cur.close()
            conn.close()
            return chatRPC_pb2.Response(text=response_message, status=status)
        
        # Get user ID if exists
        data = {
            'username': request.blocked_user
        }
        query = 'SELECT user_id FROM User WHERE username=%(username)s;'
        cur.execute(query, data)
        
        if cur.rowcount == 0:
            response_message = 'User does not exist.'
            cur.close()
            conn.close()
            status = True
            return chatRPC_pb2.Response(text=response_message, status=status)
        
        # Block/Unblock user
        data = {
            'user_id': user[0],
            'block_id': cur.fetchone()[0]
        }
        if block:
            query = 'INSERT INTO Block (user_id, block_id) VALUES (%(user_id)s, %(block_id)s);'
            response_message = 'User blocked.'
        else:
            query = 'DELETE FROM Block WHERE user_id=%(user_id)s AND block_id=%(block_id)s;'
            response_message = 'User unblocked.'
        cur.execute(query, data)
        conn.commit()

        cur.close()
        conn.close()
        status = True
        return chatRPC_pb2.Response(text=response_message, status=status)
    
    def watch_helper(self, request, watch):
        response_message = ''
        conn, cur = self.get_db()
        # Check if logged in
        user = self.get_user(conn, cur, request.access_token)
        if user == None:
            response_message = 'Unauthenticated.'
            status = False
            cur.close()
            conn.close()
            return chatRPC_pb2.Response(text=response_message, status=status)
        
        # Get Channel ID if exists
        data = {
            'channel': request.channel_name
        }
        query = 'SELECT id FROM Channel WHERE channel_name=%(channel)s;'
        cur.execute(query, data)

        if cur.rowcount == 0:
            response_message = 'Channel does not exist.'
            cur.close()
            conn.close()
            status = True
            return chatRPC_pb2.Response(text=response_message, status=status)
        
        # Watch/Unwatch channel
        data = {
            'user_id': user[0],
            'channel_id': cur.fetchone()[0],
        }
        if watch:
            query = 'INSERT INTO Watching (user_id, channel_id) VALUES (%(user_id)s, %(channel_id)s);'
            response_message = 'Watching channel.'
        else:
            query = 'DELETE FROM Watching WHERE user_id=%(user_id)s AND channel_id=%(channel_id)s;'
            response_message = 'Unwatching channel.'
        cur.execute(query, data)
        conn.commit()

        cur.close()
        conn.close()
        status = True
        return chatRPC_pb2.Response(text=response_message, status=status)

    def MessageStream(self, request_iterator, ctx):
        last_index = 0
        while True:
            while len(self.chats) > last_index:
                message = self.chats[last_index]
                last_index += 1
                yield message

    def RegisterUser(self, request, ctx):
        conn, cur = self.get_db()

        data = {
            'username': request.username,
            'password': request.password
        }
        query = 'INSERT INTO User (username, password) VALUES (%(username)s, %(password)s);'

        # Create User, if user exists then fail
        try:
            cur.execute(query, data)
            conn.commit()
        except:
            response_message = 'User already exists.'
            status = False
            cur.close()
            conn.close()
            return chatRPC_pb2.Response(text=response_message, status=status)
        
        response_message = 'Account successfully registered.'
        status = True
        cur.close()
        conn.close()

        return chatRPC_pb2.Response(text=response_message, status=status)

    def Login(self, request, ctx):
        conn, cur = self.get_db()

        # Confirm user exists
        data = {
            'username': request.username,
            'password': request.password
        }
        query = 'SELECT id FROM User WHERE username=%(username)s AND password=%(password)s;'
        cur.execute(query, data)
        
        if cur.rowcount == 0:
            response_message = 'Incorrect login info.'
            status = False
            cur.close()
            conn.close()
            return chatRPC_pb2.Response(text=response_message, status=status)

        # Check if user has access token (did not log out)
        data = {
            'id': cur.fetchone()[0]
        }
        query = 'SELECT user_id, access_token FROM Online WHERE user_id=%(id)s;'
        cur.execute(query, data)

        # If access token exists then return it
        if cur.rowcount > 0:
            response_message = cur.fetchone()[1]
            status = True
            self.get_missed_messages(data['id'], cur, conn)
            cur.close()
            conn.close()
            return chatRPC_pb2.Response(text=response_message, status=status)
        
        # If new login, create token and return to user
        data['token'] = str(hash(username + password) % (10 ** 20))
        query = 'INSERT INTO Online (user_id, access_token) VALUES(%(id)s, %(token)s);'
        cur.execute(query, data)
        conn.commit()

        access_token = data['token']
        status = True
        self.get_missed_messages(data['id'], cur, conn) # Get missed messages
        cur.close()
        conn.close()
        return chatRPC_pb2.Response(text=access_token, status=status)
    
    def Logout(self, request, ctx):
        conn, cur = self.get_db()

        # Remove user from Online sessions
        data = {
            'token': request.access_token
        }
        query = 'DELETE FROM Online WHERE access_token=%(token)s;'
        cur.execute(query, data)
        conn.commit()

        response_message = 'User logged out.'
        status = True
        cur.close()
        conn.close()
        return chatRPC_pb2.Response(text=response_message, status=status)

    def DirectMessage(self, request, ctx):
        conn, cur = self.get_db()
        # Check if logged in
        user = self.get_user(conn, cur, request.access_token)
        if user == None:
            response_message = 'Unauthenticated.'
            status = False
            cur.close()
            conn.close()
            return chatRPC_pb2.Response(text=response_message, status=status)

        # Get recipient user ID if exists
        data = {
            'recipient': request.recipient
        }
        query = 'SELECT id FROM User WHERE username=%(recipient)s;'
        cur.execute(query, data)

        if cur.rowcount == 0:
            response_message = 'Recipient does not exist.'
            status = False
            cur.close()
            conn.close()
            return chatRPC_pb2.Response(text=response_message, status=status)
        
        recipient_id = cur.fetchone()[0]
        data = {
            'id': recipient_id
        }
        query = 'SELECT user_id FROM Online WHERE user_id=%(id)s;'
        cur.execute(query, data)

        if self.is_blocked(conn, cur, user[0], recipient_id):
            response_message = 'User is blocked.'
            status = False
            cur.close()
            conn.close()
            return chatRPC_pb2.Response(text=response_message, status=status)

        # If user is offline then save message to send later, else send it
        if cur.rowcount == 0:
            data = {
                'id': recipient_id,
                'message': request.message,
                'from_user': 1,
                'sender': user[1],
                'datetime': datetime.now().date()
            }
            query = 'INSERT INTO Missed (user_id, message, from_user, sender_name, datetime) VALUES (%(id)s, %(message)s, %(from_user)s, %(sender)s, %(datetime)s);'
            cur.execute()
            conn.commit()
            response_message = 'User offline, message stored.'
        else:
            response_message = 'User online, message sent.'
            # TODO: User online, send message with Kafka
        
        cur.close()
        conn.close()
        status = True
        return chatRPC_pb2.Response(text=response_message, status=status)    
    
    def ChannelPost(self, request, ctx):
        conn, cur = self.get_db()
        # Check if logged in
        user = self.get_user(conn, cur, request.access_token)
        if user == None:
            response_message = 'Unauthenticated.'
            status = False
            cur.close()
            conn.close()
            return chatRPC_pb2.Response(text=response_message, status=status)
        
        # If channel exists then get channel ID
        data = {
            'channel': request.channel_name
        }
        query = 'SELECT id FROM Channel WHERE channel_name=%(channel)s;'
        cur.execute(query, data)

        if cur.rowcount == 0:
            response_message = 'Channel ' + request.channel_name + ' does not exist.'
            cur.close()
            conn.close()
            status = True
            return chatRPC_pb2.Response(text=response_message, status=status)
        
        # Get list of users in channel
        data = {
            'id': cur.fetchone()[0]
        }
        query = 'SELECT user_id FROM Watching WHERE channel_id=%(id)s;'
        cur.execute()
        
        recipient_list = cur.fetchall()
        online_list = []

        # Get list of online users
        for recipient in recipient_list:
            data = {
                'id': recipient
            }
            query = 'SELECT * FROM Online WHERE user_id=%(id)s;'
            cur.execute()

            if cur.rowcount > 0:
                online_list.append(recipient)
        
        # Get list of offline users
        offline_list = list(set(recipient_list) - set(online_list))

        # Send messages to online users
        for recipient in online_list:
            if self.is_blocked(conn, cur, user[0], recipient):
                continue
            # TODO: User online, send message with Kafka
        
        # Store messages for offline users
        for recipient in offline_list:
            if self.is_blocked(conn, cur, user[0], recipient):
                continue
            data = {
                'id': recipient,
                'message': request.message,
                'from_user': 0,
                'sender': user[1],
                'datetime': datetime.now().date()
            }
            query = 'INSERT INTO Missed (user_id, message, from_user, sender_name, datetime) VALUES (%(id)s, %(message)s, %(from_user)s, %(sender)s, %(datetime)s);'
            cur.execute()
            conn.commit()
        
        response_message = 'Message sent to channel.'
        cur.close()
        conn.close()
        status = True
        return chatRPC_pb2.Response(text=response_message, status=status)

    def Block(self, request, ctx):
        return self.block_helper(request, True)

    def Unblock(self, request, ctx):
        return self.block_helper(request, False)

    def Watch(self, request, ctx):
        return self.watch_helper(request, True)

    def Unwatch(self, request, ctx):
        return self.watch_helper(request, False)

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    chatRPC_pb2_grpc.add_ChatServiceServicer_to_server(ChatAppManager(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()

server()
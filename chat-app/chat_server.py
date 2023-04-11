
from concurrent import futures
import grpc
import chatRPC_pb2
import chatRPC_pb2_grpc
import sys
import os
import mysql.connector as db


class ChatAppManager(chatRPC_pb2_grpc.ChatServiceServicer):

    def __init__(self):
        self.conn = db.connect(host='localhost', port=3306, user='root', password=os.environ.get('MYSQL_PASSWORD'))
        self.cur = self.conn.cursor()



    def RegisterUser(self, request, context):
        user_id = request.user_id
        password = request.password

        # needs key

        sql = "insert into users values(?, ?, NULL, datetime('now'), 0)"
        params = (user_id, password)

        try:
            cur.execute(sql, params)
            conn.commit()

            response_message = "Your account was successfully registered."
            status = True

        except Error as e:

            response_message = "This username already exists, please use another username."
            status = False

        return chatRPC_pb2.Response(text =  response_message,status = status)

    def Login(self,request, context):

        user_id = request.user_id
        password = request.password

        sql = "select id, password,key from users where id = ?"
        params = (user_id,)
        cur.execute(sql,params)

        row = cur.fetchall()

        if not row:
            return chatRPC_pb2.Response(text = "User does not exist", status = False)
        
        else:
            
            row = row[0]

            if password == row[1]:
                
                key = row[2]

                set_online_sql = "update users set onlineoffline = 1 where id = ?"
                params = (user_id,)

                cur.execute(set_online_sql, params)
                conn.commit()

                return chatRPC_pb2.Response(text = key, status = True) # SUCCESS
            
            else:

                return chatRPC_pb2.Response(text = "Incorrect Password", status = False)


    def DirectMessage(self, request, context):

        sender = request.sender_id
        recipient = request.recipient
        message = request.message
        key = request.key

        params = (sender,)

        check_key_sql = "select key, onlineoffline from users where id =?"

        cur.execute(check_key_sql,params)

        key_row = cur.fetchall()

        if not key_row:
            
            return chatRPC_pb2.Response(text = "User does not exist.", status = False)

        else:

            key_row = key_row[0]

            if key != key_row[0]:

                return chatRPC_pb2.Response(text = "Incorrect Key", status = False)

            elif key == key_row[0]:

                # check_online_sql = "select onlineoffline from users where id = ?"
                # params = (recipient,)

                # cur.execute(check_online_sql, params)

                # online_row = cur.fetchall()

                online_row = key_row[1]

                if online_row == 0:

                    insert_dm_sql = "insert into messages values(?, ?, NULL, ?, datetime('now'), 0)"

                    try:
                        params = (sender, recipient, message)

                        cur.execute(insert_dm_sql, params)
                        conn.commit()

                        return chatRPC_pb2.Response(text = "User is not online, stored message", status = False) # STORED

                    
                    except Error as e:

                        return chatRPC_pb2.Response(text = "Error: Failed to store message", status = False)
                
                elif online_row == 1:
                    
                    insert_dm_sql = "insert into messages values(?, ?, NULL, ?, datetime('now'), 1)"

                    try:
                        params = (sender, recipient, message)

                        cur.execute(insert_dm_sql, params)
                        conn.commit()

                        return chatRPC_pb2.Response(text = "sent_message", status = True) # SUCCESS

                    
                    except Error as e:

                        return chatRPC_pb2.Response(text = "Error: Failed to send message", status = False)
    
    
    def ChannelPost(self, request, context):

        """
         string user_id = 1;
        string channel = 2;
        string message = 3;
        string key = 4;
        """

        user_id = request.user_id
        channel = request.channel
        message = request.message
        key = request.key

        check_key_sql = "select key from users where id =?"
        params = (sender,)

        cur.execute(check_key_sql,params)

        key_row = cur.fetchall()

        if not key_row:
            
            return chatRPC_pb2.Response(text = "User does not exist.", status = False)

        else:

            key_row = key_row[0]

            if key != key_row[0]:

                return chatRPC_pb2.Response(text = "Incorrect Key", status = False)

            elif key == key_row[0]:
                
                check_channel_exists_sql = "select name from channels where name = ?"
                params = (channel,)

                cur.execute(check_channel_exists_sql, params)
                
                channel_row = cur.fetchall()

                if not channel_row:

                    return chatRPC_pb2.Response(text = "Channel does not exist", status = False)
                
                else:

                    channel_row = channel_row[0]

                    channel_msg_sql = "insert into messages values(?, NULL, ?, ?, datetime('now'), 1)"

                    try:
                        
                        params = (sender, channel, message)

                        cur.execute(channel_msg_sql, params)
                        conn.commit()

                        return chatRPC_pb2.Response(text = "sent_message", status = True) # SUCCESS

                    
                    except Error as e:

                        return chatRPC_pb2.Response(text = "Error: Failed to post to channel", status = False)

    def Block(self, request, context):

        # string blocker_id = 1;
        # string blocked_id = 2;

        blocker = request.blocker_id
        blocked = request.blocked_id

        check_key_sql = "select key from users where id =?"
        params = (sender,)

        cur.execute(check_key_sql,params)

        key_row = cur.fetchall()

        if not key_row:
            
            return chatRPC_pb2.Response(text = "User does not exist.", status = False)

        else:

            key_row = key_row[0]

            if key != key_row[0]:

                return chatRPC_pb2.Response(text = "Incorrect Key", status = False)

            elif key == key_row[0]:

                check_blocker_id = "select id from users where id = ?"
                params = (blocker,)

                cur.execute(check_blocker_id, params)
                blocker_row = cur.fetchall()

                if not blocker_row:

                    return chatRPC_pb2.Response(text = "Blocker user ID does not exist", status = False)

                check_blocked_id = "select id from users where id = ?"
                params = (blocked,)

                cur.execute(check_blocked_id, params)
                blocked_row = cur.fetchall()

                if not blocked_row:

                    return chatRPC_pb2.Response(text = "Blocked user ID does not exist", status = False)

                block_sql = "insert into blocks values(?, ?, datetime('now'))"
                params = (blocker, blocked)

                try:

                    cur.execute(block_sql, params)
                    conn.commit()

                    return chatRPC_pb2.Response(text = "Blocked User", status = True) # SUCCESS

                
                except Error as e:

                    return chatRPC_pb2.Response(text = "Error: Failed to record block", status = False)

    def Unblock(self, request, context):

        # string blocker_id = 1;
        # string blocked_id = 2;

        blocker = request.blocker_id
        blocked = request.blocked_id

        check_key_sql = "select key from users where id =?"
        params = (sender,)

        cur.execute(check_key_sql,params)

        key_row = cur.fetchall()

        if not key_row:
            
            return chatRPC_pb2.Response(text = "User does not exist.", status = False)

        else:

            key_row = key_row[0]

            if key != key_row[0]:

                return chatRPC_pb2.Response(text = "Incorrect Key", status = False)

            elif key == key_row[0]:

                check_blocker_id = "select id from users where id = ?"
                params = (blocker,)

                cur.execute(check_blocker_id, params)
                blocker_row = cur.fetchall()

                if not blocker_row:

                    return chatRPC_pb2.Response(text = "Blocker user ID does not exist", status = False)

                check_blocked_id = "select id from users where id = ?"
                params = (blocked,)

                cur.execute(check_blocked_id, params)
                blocked_row = cur.fetchall()

                if not blocked_row:

                    return chatRPC_pb2.Response(text = "Blocked user ID does not exist", status = False)

                block_sql = "delete from blocks where blocking_user = ? and blocked_user = ?"
                params = (blocker, blocked)

                try:

                    cur.execute(block_sql, params)
                    conn.commit()

                    return chatRPC_pb2.Response(text = "Unblocked user", status = True) # SUCCESS

                
                except Error as e:

                    return chatRPC_pb2.Response(text = "Error: Failed to remove block from record", status = False)

    
    def Watch(self, request_iterator, context):

        """
        message watch{
        string user_id = 1;
        string channel = 2;
        }
        lastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n
        """

        user_id = request.user_id
        channel = request.channel

        check_key_sql = "select key from users where id =?"
        params = (sender,)

        cur.execute(check_key_sql,params)

        key_row = cur.fetchall()

        if not key_row:
            
            return chatRPC_pb2.Response(text = "User does not exist.", status = False)

        else:

            key_row = key_row[0]

            if key != key_row[0]:

                return chatRPC_pb2.Response(text = "Incorrect Key", status = False)

            elif key == key_row[0]:
                
                check_channel_exists_sql = "select name from channels where name = ?"
                params = (channel,)

                cur.execute(check_channel_exists_sql, params)
                
                channel_row = cur.fetchall()

                if not channel_row:

                    return chatRPC_pb2.Response(text = "Channel does not exist", status = False)
                
                else:

                    lastindex = 0

                    add_sub_sql = "insert into subscriptions values(?, ?, datetime('now'))"
                    params = (channel, user_id)

                    try:
                        cur.execute(add_sub_sql, params)
                        conn.commit()

                    except Error as e:
                        
                        return chatRPC_pb2.Response(text = "Error: failed to record subscription", status = False)

                    while True:



                        get_channel_posts_sql = "select sender, message from messages where channel = ?"
                        params = (channel,)

                        cur.execute(get_channel_posts_sql, params)

                        messages_read = cur.fetchall()

                        for msg in messages_read:
                            
                            self.channel_posts.append(msg)
                        
                        while len(self.channel_posts) > lastindex:

                            n = self.channel_posts[lastindex]
                            lastindex += 1
                            yield n

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    chatRPC_pb2_grpc.add_ChatServiceServicer_to_server(ChatAppManager, server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()

server()
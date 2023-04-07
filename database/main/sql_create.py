import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)



if __name__ == '__main__':
    
    conn = create_connection(r"chatDB.db")

    create_users_table = "create table if not exists users (id text, password text, access_key text register_date datetime, PRIMARY KEY (id, access_key))"
    create_channels_table = "create table if not exists channels (name text PRIMARY KEY, creation_date datetime)"
    create_subscriptions_table = "create table if not exists subscriptions (channel_name text, user_id text, subscription_date datetime, PRIMARY KEY (channel_name, user_id))"
    create_blocks_table = "create table if not exists blocks (blocking_user text, blocked_user text, block_date datetime, PRIMARY KEY (blocking_user, blocked_user))"

    """
    add new user: insert into users values(A, B, C, datetime(now))

    check if channel exists: select name from channels where name = X

    check if user exists: select id from users where id = X

    check if user is blocked: select blocked_user from blocks where blocking_user = A and blocked_user = B

    add subscription: insert into subscriptions values (A, B, datetime(now))

    remove subscription: delete from subscriptions where channel name = A and user_id = B

    block user: insert into blocks values (A, B, datetime(now))

    unblock user: delete from blocks where blocking_user = A and blocked_user = B

    """
    
    if conn is not None:
        
        create_table(conn, create_users_table)

        create_table(conn, create_channels_table)

        create_table(conn, create_subscriptions_table)
        
        create_table(conn, create_blocks_table)
    else:
        print("Error! cannot create the database connection.")

    
# Startup Instructions
1. Install Docker and Python 3.x.x
2. Run `docker-compose up --build --scale chat-app=3`
    1. To add more change nginx conf by increasing servers behind proxy
3. Run `python3 /chat-app/chat-client.py` two or more times in separate terminals

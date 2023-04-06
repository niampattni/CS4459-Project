# Startup Instructions
1. Install Docker
2. Run `docker-compose up --build --scale chat-app=3`
    1. We can change the number of docker containers to anything here, currently Nginx is set up for 3 instances
3. Send requests through http://localhost:5001

FROM python:latest
ENV MYSQL_PASSWORD=pass
WORKDIR /usr/src/chat-app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "chat_server.py"]
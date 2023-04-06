FROM python:latest
WORKDIR /usr/src/chat-app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
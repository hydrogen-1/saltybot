FROM python:3.9.18-slim

RUN pip install websocket-client
WORKDIR /src
COPY / /src

ENTRYPOINT [ "python", "-u", "main.py" ]
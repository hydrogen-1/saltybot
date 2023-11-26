FROM python:3.9.18-slim

RUN pip install websocket-client
RUN pip install -i https://test.pypi.org/simple/ twitchchat-wss
WORKDIR /src
COPY / /src

ENTRYPOINT [ "python", "-u", "main.py" ]
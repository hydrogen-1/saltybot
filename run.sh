#!/bin/sh
docker run -d\
    --mount type=bind,source="$(pwd)"/players.db,target=/src/players.db \
    --mount type=bind,source="$(pwd)"/login.json,target=/src/login.json,readonly \
    --restart=unless-stopped \
    saltybot:latest
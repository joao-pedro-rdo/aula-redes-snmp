#!/bin/bash
docker compose -f compose-server.yml run tcp-server

python3 tcp-server/tcp-server.py
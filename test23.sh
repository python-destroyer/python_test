#!/bin/bash
python test2/Server_to_receive_CSV/main.py &
python test2/The_task/main.py &
python test3/http_server/main.py 

#!/bin/bash
if pgrep -f '/home/deploy/apps/goods_hunter/venv/bin/python /home/deploy/apps/goods_hunter/current/parse.py' > /dev/null
then
    echo "Running"
    # pgrep -f '/home/deploy/venv/bin/python /home/deploy/apps/topsale/current/parse.py' | xargs kill
else
    echo "Stopped"
    nohup /home/deploy/apps/goods_hunter/venv/bin/python /home/deploy/apps/goods_hunter/current/parse.py &
fi

#!/bin/sh

LOG="/mnt/mmc/MUOS/init/start-autobt_log.txt"

echo "Launching autobt" >> "$LOG"

python3 /mnt/mmc/MUOS/application/autobt_banana.py &

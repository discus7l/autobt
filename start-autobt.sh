#!/bin/sh

LOG="/mnt/mmc/MUOS/init/start-autobt_log.txt"

echo "Launching autobt" >> "$LOG"

python /mnt/mmc/MUOS/application/autobt.py &

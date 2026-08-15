#!/bin/sh

LOG="/mnt/mmc/MUOS/init/start-autobt_log.txt"

echo "Launching autobt" >> "$LOG"

/mnt/mmc/MUOS/application/autobt.sh &

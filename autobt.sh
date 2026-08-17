#!/bin/sh

LOG="/mnt/mmc/MUOS/application/autobt_log.txt"
FLAG="/mnt/mmc/MUOS/application/autobt_flag.txt"
MAX_RETRIES=30
RETRY_DELAY=3
SINK_TIMEOUT=3

count=1

rm -f "$FLAG"

echo "[$(date)] Starting autobt" >> "$LOG"

sleep 15

while [ "$count" -le "$MAX_RETRIES" ]; do
    echo "[$(date)] Checking Bluetooth connection (attempt $count/$MAX_RETRIES)..." >> "$LOG"
    CONNECTED=$(bluetoothctl devices Connected)
    echo "$CONNECTED" | while read -r _ _ NAME; do
        echo $NAME
        if [ -n "$NAME" ]; then
            echo "[$(date)] $NAME connected." >> "$LOG"

            # Wait for PipeWire to detect the device sink
            timeout=0
            while [ "$timeout" -lt "$SINK_TIMEOUT" ]; do
                echo "[$(date)] Checking $NAME sink (timeout: $timeout/$SINK_TIMEOUT)..." >> "$LOG"
                SINK_LINE=$(wpctl status | grep "$NAME" | grep "vol")
                echo "[$(date)] PipeWire status: $SINK_LINE" >> "$LOG"

                # If PipeWire sink is detected, set ID as the default and exit
                if [ -n "$SINK_LINE" ]; then
                    echo "[$(date)] PipeWire sink for $NAME detected." >> "$LOG"
                    ID=$(echo "$SINK_LINE" | sed -n "s/.*[[:space:]]\([0-9][0-9]*\)\. $NAME.*/\1/p")
                    echo "[$(date)] Found sink ID: $ID" >> "$LOG"
                    wpctl set-default "$ID"
                    echo "[$(date)] Default sink set." >> "$LOG"
                    touch "$FLAG"
                    break
                fi

                sleep 1
                timeout=$((timeout + 1))
            done
        else
            echo "[$(date)] Waiting for devices to connect." >> "$LOG"
        fi
    done

    # Check if the flag file was created, indicating a successful connection and default sink set
    if [ -f "$FLAG" ]; then
        echo "[$(date)] Bluetooth audio device connected and default sink set." >> "$LOG"
        rm -f "$FLAG"
        exit 0
    fi

    sleep "$RETRY_DELAY"
    count=$((count + 1))
done

echo "[$(date)] Bluetooth audio device never connected." >> "$LOG"
rm -f "$FLAG"
exit 1

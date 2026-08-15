#!/bin/sh

LOG="/mnt/mmc/MUOS/application/autobt_log.txt"
TARGET_DEVICE="Device 74:DE:8D:38:BD:C1 TX612"
MAX_RETRIES=10
RETRY_DELAY=3
SINK_TIMEOUT=15

count=1

echo "Starting autobt" >> "$LOG"
sleep 10

while [ "$count" -le "$MAX_RETRIES" ]; do
    echo "Checking Bluetooth connection (attempt $count/$MAX_RETRIES)..." >> "$LOG"

    CONNECTED=$(bluetoothctl devices Connected)

    if [ "$CONNECTED" = "$TARGET_DEVICE" ]; then
        echo "TX612 connected." >> "$LOG"

        # Wait for PipeWire to detect the TX612 sink
        timeout=0
        until wpctl status | grep -q "TX612.*vol"; do
            sleep 1
            timeout=$((timeout + 1))

            if [ "$timeout" -ge "$SINK_TIMEOUT" ]; then
                echo "Timed out waiting for TX612 sink." >> "$LOG"
                exit 1
            fi
        done

        SINK_LINE=$(wpctl status | grep "TX612" | grep "vol")

        if [ -n "$SINK_LINE" ]; then
            ID=$(echo "$SINK_LINE" | sed -n 's/.*[[:space:]]\([0-9][0-9]*\)\. TX612.*/\1/p')

            echo "Found sink ID: $ID" >> "$LOG"

            wpctl set-default "$ID"

            echo "Default sink set." >> "$LOG"

            exit 0
        else
            echo "TX612 sink not found in PipeWire." >> "$LOG"
            exit 1
        fi
    fi

    sleep "$RETRY_DELAY"
    count=$((count + 1))
done

echo "TX612 never connected." >> "$LOG"
exit 1

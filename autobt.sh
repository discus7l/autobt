#!/bin/sh

TARGET_DEVICE="Device 74:DE:8D:38:BD:C1 TX612"
MAX_RETRIES=5
RETRY_DELAY=3
SINK_TIMEOUT=15

count=1

echo "Starting autobt" > /mnt/mmc/MUOS/init/autobt_log.txt

while [ "$count" -le "$MAX_RETRIES" ]; do
    echo "Checking Bluetooth connection (attempt $count/$MAX_RETRIES)..."

    CONNECTED=$(bluetoothctl devices Connected)

    if [ "$CONNECTED" = "$TARGET_DEVICE" ]; then
        echo "TX612 connected."

        # Wait for PipeWire to detect the TX612 sink
        timeout=0
        until wpctl status | grep -q "TX612.*vol"; do
            sleep 1
            timeout=$((timeout + 1))

            if [ "$timeout" -ge "$SINK_TIMEOUT" ]; then
                echo "Timed out waiting for TX612 sink."
                exit 1
            fi
        done

        SINK_LINE=$(wpctl status | grep "TX612" | grep "vol")

        if [ -n "$SINK_LINE" ]; then
            ID=$(echo "$SINK_LINE" | awk '{gsub(/\./,"",$1); print $1}')

            echo "Found sink ID: $ID"

            wpctl set-default "$ID"

            echo "Default sink set."

            exit 0
        else
            echo "TX612 sink not found in PipeWire."
            exit 1
        fi
    fi

    sleep "$RETRY_DELAY"
    count=$((count + 1))
done

echo "TX612 never connected."
exit 1
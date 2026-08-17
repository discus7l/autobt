#!/bin/sh

LOCAL_FILE="/home/yk/Documents/github/autobt/autobt/autobt.sh"
REMOTE_FILE="/mnt/mmc/MUOS/application/autobt.sh"
REMOTE_HOST="192.168.10.9"

# Copy local file and set permissions on the remote host
scp $LOCAL_FILE root@$REMOTE_HOST:$REMOTE_FILE
echo "File copied to remote host..."

ssh root@$REMOTE_HOST "chmod +x $REMOTE_FILE"
echo "File permissions set..."

# Remove log file on the remote host
ssh root@$REMOTE_HOST "rm -f /mnt/mmc/MUOS/application/autobt_log.txt"
echo "Log file removed on remote host..."

# Execute the script on the remote host
# ssh root@$REMOTE_HOST "sh $REMOTE_FILE"
# echo "Executed script on remote host: $REMOTE_HOST:$REMOTE_FILE"

exit 0

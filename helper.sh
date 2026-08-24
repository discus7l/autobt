#!/bin/sh

LOCAL_FILE="/home/yk/Documents/github/autobt/autobt/autobt.py"
LOCAL_START_FILE="/home/yk/Documents/github/autobt/autobt/start-autobt.sh"
LOCAL_CONF_FILE="/home/yk/Documents/github/autobt/autobt/autobt_conf.ini"

REMOTE_FILE="/mnt/mmc/MUOS/application/autobt.py"
REMOTE_START_FILE="/mnt/mmc/MUOS/init/start-autobt.sh"
REMOTE_CONF_FILE="/mnt/mmc/MUOS/application/autobt_conf.ini"

REMOTE_HOST="192.168.10.9"

# Copy local file
scp $LOCAL_FILE root@$REMOTE_HOST:$REMOTE_FILE
scp $LOCAL_START_FILE root@$REMOTE_HOST:$REMOTE_START_FILE
scp $LOCAL_CONF_FILE root@$REMOTE_HOST:$REMOTE_CONF_FILE
echo "Files copied to remote host..."

#  Set permissions on the remote host
ssh root@$REMOTE_HOST "chmod +x $REMOTE_FILE"
ssh root@$REMOTE_HOST "chmod +x $REMOTE_START_FILE"
echo "File permissions set..."

# Remove log file on the remote host
ssh root@$REMOTE_HOST "rm -f /mnt/mmc/MUOS/application/autobt.log"
echo "Log file removed on remote host..."

# Execute the script on the remote host
# ssh root@$REMOTE_HOST "sh $REMOTE_FILE"
# echo "Executed script on remote host: $REMOTE_HOST:$REMOTE_FILE"

exit 0

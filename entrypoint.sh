#!/bin/bash
set -e

if [ -z "$CRON_SCHEDULE" ]; then
    echo "ERROR: \$CRON_SCHEDULE not set!"
    exit 1
fi

# Write cron schedule
echo "$CRON_SCHEDULE /backup/backup.sh > /dev/stdout" >> /var/spool/cron/crontabs/root

exec "$@"

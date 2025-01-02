#!/bin/bash
set -e

if [[ $@ == *crond* ]] && [ -z "$CRON_SCHEDULE" ]; then
    echo "ERROR: \$CRON_SCHEDULE not set!"
    exit 1
fi

# Write cron schedule
echo "$CRON_SCHEDULE python3 -u /backup/backup.py > /dev/stdout" | crontab -

exec "$@"

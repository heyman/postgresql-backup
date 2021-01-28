#!/bin/bash
set -e

if [[ $@ == crond* ]] && [ -z "$CRON_SCHEDULE" ]; then
    echo "ERROR: \$CRON_SCHEDULE not set!"
    exit 1
fi

# Write cron schedule
echo "$CRON_SCHEDULE python -u /backup/backup.py > /dev/stdout" >> /var/spool/cron/crontabs/root

exec "$@"

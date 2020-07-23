#!/bin/bash

set -e

function run_backup() {
  local database=$(echo $1 | tr ':' ' ' | awk '{print $1}')
  local user=$(echo $1 | tr ':' ' ' | awk '{print $2}')
  local pass=$(echo $1 | tr ':' ' ' | awk '{print $3}')
  echo "backuping ${database}"
  DB_NAME=$database DB_USER=$user DB_PASS=$pass python -u /backup/backup.py
}

if [ -n "$DBS" ]; then
  for db in $(echo $DBS | tr ',' ' '); do
    run_backup $db
  done
else
  python -u /backup/backup.py
fi

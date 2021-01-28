# Docker PostgreSQL Backup

[![Build Status](https://github.com/heyman/postgresql-backup/workflows/Test/badge.svg)](https://github.com/heyman/postgresql-backup/actions?query=workflow%3ATest)

Docker image that periodically dumps a Postgres database, and uploads it to an Amazon S3 bucket.

## Required environment variables

* `CRON_SCHEDULE`: The time schedule part of a crontab file (e.g: `15 3 * * *` for every night 03:15)
* `DB_HOST`: Postgres hostname
* `DB_PASS`: Postgres password
* `DB_USER`: Postgres username
* `DB_NAME`: Name of database
* `S3_PATH`: Amazon S3 path in the format: s3://bucket-name/some/path
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_DEFAULT_REGION`

## Optional environment variables

* `MAIL_TO`: If `MAIL_TO` and `MAIL_FROM` is specified, an e-mail will be sent, using Amazon SES, every time a backup is taken
* `MAIL_FROM`
* `WEBHOOK`: If specified, an HTTP request will be sent to this URL
* `WEBHOOK_METHOD`: By default the webhook's HTTP method is GET, but can be changed using this variable
* `KEEP_BACKUP_DAYS`: The number of days to keep backups for when pruning old backups. Defaults to `7`.
* `FILENAME`: String that is passed into `strftime()` and used as the backup dump's filename. Defaults to `$DB_NAME_%Y-%m-%d`.

## Volumes

* `/data/backups` - The database is dumped in into this directory

## Restoring a backup

This image can also be run as a one off task to restore one of the backups. 
To do this, we run the container with the command: `python -u /backup/restore.py [S3-filename]` 
(`S3-filename` should only be the name of the file, the directory is set through the `S3_PATH` env variable).

The following environment variables are required:

* `DB_HOST`: Postgres hostname
* `DB_PASS`: Postgres password
* `DB_USER`: Postgres username
* `DB_NAME`: Name of database to import into
* `S3_PATH`: Amazon S3 directory path in the format: s3://bucket-name/some/path
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_DEFAULT_REGION`

## Taking a one off backup

To run a one off backup job, e.g. to test that it works when setting it up for the first time, simply start 
the container with the docker run command set to `python -u backup.py` (as well as all the required environment 
variables set).


## Docker tags

This image uses the alpine version(s) of the [official postgres](https://hub.docker.com/_/postgres) image as base 
image.

The following docker tags are available for this image, and they are based on the corresponding official postgres 
alpine image:

* `13`, `latest`
* `12`
* `11`
* `10`

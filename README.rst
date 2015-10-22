=========================
Docker PostgresSQL Backup
=========================

Docker image that runs a cron job which dumps a Postgres database, and uploads it to an Amazon S3 bucket.

Required environment variables
==============================

*CRON_SCHEDULE*: The time schedule part of a crontab file (e.g: "15 3 * * *" for every night 03:15)
*DB_HOST*: Postgres hostname
*DB_PASS*: Postgres password
*DB_USER*: Postgres username
*DB_NAME*: Name of database

*S3_PATH*: Amazon S3 path in the format: s3://bucket-name/some/path
*AWS_ACCESS_KEY_ID*
*AWS_SECRET_ACCESS_KEY*
*AWS_DEFAULT_REGION*

Optional environment variables
==============================

*MAIL_TO*: If MAIL_TO and MAIL_FROM is specified, an e-mail will be sent, using Amazon SES, every time a backup is taken
*MAIL_FROM*

*WEBHOOK*: If specified, an HTTP request will be sent to this URL
*WEBHOOK_METHOD*: By default the webhook's HTTP method is GET, but can be changed using this variable

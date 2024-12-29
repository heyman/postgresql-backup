#!/usr/bin/python3

import os
import subprocess
import sys
from datetime import datetime

dt = datetime.now()

BACKUP_DIR = os.environ["BACKUP_DIR"]

S3_PATH = os.environ.get("S3_PATH", "")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_STORAGE_CLASS = os.environ.get("S3_STORAGE_CLASS", "STANDARD_IA")
S3_EXTRA_OPTIONS = os.environ.get("S3_EXTRA_OPTIONS", "")

DB_USE_ENV = os.environ.get("DB_USE_ENV", False)
DB_NAME = os.environ["DB_NAME"] if "DB_NAME" in os.environ else os.environ.get("PGDATABASE")

if not DB_NAME:
    raise Exception("DB_NAME must be set")

if not DB_USE_ENV:
    DB_HOST = os.environ["DB_HOST"]
    DB_PASS = os.environ["DB_PASS"]
    DB_USER = os.environ["DB_USER"]
    DB_PORT = os.environ.get("DB_PORT", "5432")

MAIL_TO = os.environ.get("MAIL_TO")
MAIL_FROM = os.environ.get("MAIL_FROM")
WEBHOOK = os.environ.get("WEBHOOK")
WEBHOOK_METHOD = os.environ.get("WEBHOOK_METHOD")
WEBHOOK_DATA = os.environ.get("WEBHOOK_DATA")
WEBHOOK_CURL_OPTIONS = os.environ.get("WEBHOOK_CURL_OPTIONS", "")
KEEP_BACKUP_DAYS = int(os.environ.get("KEEP_BACKUP_DAYS", 7))
FILENAME = os.environ.get("FILENAME", DB_NAME + "_%Y-%m-%d")
PG_DUMP_EXTRA_OPTIONS = os.environ.get("PG_DUMP_EXTRA_OPTIONS", "")

file_name = dt.strftime(FILENAME)
backup_file = os.path.join(BACKUP_DIR, file_name)

if not S3_PATH.endswith("/"):
    S3_PATH = S3_PATH + "/"

if WEBHOOK_DATA and not WEBHOOK_METHOD:
    WEBHOOK_METHOD = 'POST'
else:
    WEBHOOK_METHOD = WEBHOOK_METHOD or 'GET'

def cmd(command, **kwargs):
    try:
        subprocess.check_output([command], shell=True, stderr=subprocess.STDOUT, **kwargs)
    except subprocess.CalledProcessError as e:
        sys.stderr.write("\n".join([
            "Command execution failed. Output:",
            "-"*80,
            e.output,
            "-"*80,
            ""
        ]))
        raise

def backup_exists():
    return os.path.exists(backup_file)

def take_backup():
    env = os.environ.copy()
    if DB_USE_ENV:
        env.update({key: os.environ[key] for key in os.environ.keys() if key.startswith('PG') })
    else:
        env.update({'PGPASSWORD': DB_PASS, 'PGHOST': DB_HOST, 'PGUSER': DB_USER, 'PGDATABASE': DB_NAME, 'PGPORT': DB_PORT})

    # trigger postgres-backup
    command = [
        "pg_dump",
        "-Fc",
    ]
    if PG_DUMP_EXTRA_OPTIONS:
        command.append(PG_DUMP_EXTRA_OPTIONS)
    command.append("> %s" % backup_file)
    cmd(" ".join(command), env=env)

def upload_backup():
    opts = "--storage-class=%s %s" % (S3_STORAGE_CLASS, S3_EXTRA_OPTIONS)
    cmd("aws s3 cp %s %s %s" % (opts, backup_file, S3_PATH))

def prune_local_backup_files():
    cmd("find %s -type f -prune -mtime +%i -exec rm -f {} \;" % (BACKUP_DIR, KEEP_BACKUP_DAYS))

def send_email(to_address, from_address, subject, body):
    """
    Super simple, doesn't do any escaping
    """
    cmd("""aws --region us-east-1 ses send-email --from %(from)s --destination '{"ToAddresses":["%(to)s"]}' --message '{"Subject":{"Data":"%(subject)s","Charset":"UTF-8"},"Body":{"Text":{"Data":"%(body)s","Charset":"UTF-8"}}}'""" % {
        "to": to_address,
        "from": from_address,
        "subject": subject,
        "body": body,
    })

def log(msg):
    print("[%s]: %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))

def pretty_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def main():
    start_time = datetime.now()
    log("Dumping database")
    take_backup()
    backup_size=os.path.getsize(backup_file)

    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        log("Uploading to S3")
        upload_backup()
    else:
        log("Skipping S3 upload, no AWS credentials provided")

    log("Pruning local backup copies")
    prune_local_backup_files()
    end_time = datetime.now()

    meta = {
        "filename": file_name,
        "date": end_time.strftime("%Y-%m-%d"),
        "time": end_time.strftime('%H:%M:%S'),
        "duration": "%.2f" % ((end_time - start_time).total_seconds()),
        "size": pretty_bytes(backup_size)
    }

    if MAIL_TO and MAIL_FROM:
        log("Sending mail to %s" % MAIL_TO)
        send_email(
            MAIL_TO,
            MAIL_FROM,
            "Backup complete: %s" % DB_NAME,
            "Took %(duration)s seconds" % meta,
        )

    if WEBHOOK:
        if WEBHOOK_DATA:
            opts = "%s -d '%s'" % (WEBHOOK_CURL_OPTIONS, WEBHOOK_DATA % meta)
        else:
            opts = WEBHOOK_CURL_OPTIONS

        log("Making HTTP %s request to webhook: %s" % (WEBHOOK_METHOD, WEBHOOK))
        cmd("curl -X %s %s %s" % (WEBHOOK_METHOD, opts, WEBHOOK))

    log("Backup complete, took %(duration)s seconds, size %(size)s" % meta)


if __name__ == "__main__":
    main()

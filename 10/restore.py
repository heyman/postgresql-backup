#!/usr/bin/python

import os
import subprocess
import sys
from datetime import datetime

BACKUP_DIR = os.environ["BACKUP_DIR"]
S3_PATH = os.environ["S3_PATH"]
DB_NAME = os.environ["DB_NAME"]
DB_PASS = os.environ["DB_PASS"]
DB_USER = os.environ["DB_USER"]
DB_HOST = os.environ["DB_HOST"]

file_name = sys.argv[1]
backup_file = os.path.join(BACKUP_DIR, file_name)

if not S3_PATH.endswith("/"):
    S3_PATH = S3_PATH + "/"

def cmd(command):
    try:
        subprocess.check_output([command], shell=True, stderr=subprocess.STDOUT)
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

def restore_backup():
    if not backup_exists():
        sys.stderr.write("Backup file doesn't exists!\n")
        sys.exit(1)
    
    # restore postgres-backup
    cmd("env PGPASSWORD=%s pg_restore -Fc -h %s -U %s -d %s %s" % (
        DB_PASS, 
        DB_HOST, 
        DB_USER, 
        DB_NAME, 
        backup_file,
    ))

def download_backup():
    cmd("aws s3 cp %s%s %s" % (S3_PATH, file_name, backup_file))

def log(msg):
    print "[%s]: %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)

def main():
    start_time = datetime.now()
    if backup_exists():
        log("Backup file already exists in filesystem %s" % backup_file)
    else:
        log("Downloading database dump")
        download_backup()
    
    log("Restoring database")
    restore_backup()
    
    log("Restore complete, took %.2f seconds" % (datetime.now() - start_time).total_seconds())

if __name__ == "__main__":
    main()

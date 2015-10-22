FROM heyman/postgresql
MAINTAINER Jonatan Heyman <http://heyman.info>

RUN apt-get update && apt-get install -y \
    python \
    python2.7 \
    python-dev \
    python-setuptools \
    awscli

VOLUME ["/data/backups"]

ENV BACKUP_DIR /data/backups

ADD . /backup
RUN touch /backup.log

ENTRYPOINT ["/backup/entrypoint.sh"]
CMD cron && tail -f /backup.log

FROM postgres:10-alpine
MAINTAINER Jonatan Heyman <http://heyman.info>

# Install dependencies
RUN apk update && apk add --no-cache --virtual .build-deps && apk add \
    bash make curl openssh git 

# Install aws-cli
RUN apk -Uuv add groff less python py-pip && pip install awscli
# Cleanup
RUN apk --purge -v del py-pip && rm /var/cache/apk/*


VOLUME ["/data/backups"]

ENV BACKUP_DIR /data/backups

ADD . /backup

ENTRYPOINT ["/backup/entrypoint.sh"]

CMD crond -f -d 8

FROM postgres:11-alpine

# Install dependencies
RUN apk update && apk add --no-cache --virtual .build-deps && apk add \
    bash make curl openssh git aws-cli

# Install python
RUN apk -Uuv add groff less python3

# Cleanup
RUN rm /var/cache/apk/*


VOLUME ["/data/backups"]

ENV BACKUP_DIR /data/backups

ADD . /backup

ENTRYPOINT ["/backup/entrypoint.sh"]

CMD crond -f -l 2

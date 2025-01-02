FROM postgres:12-alpine

# Install dependencies
RUN apk add --no-cache -uv curl aws-cli python3

VOLUME ["/data/backups"]

ENV BACKUP_DIR=/data/backups

ADD . /backup

ENTRYPOINT ["/backup/entrypoint.sh"]

CMD ["crond", "-f", "-l", "2"]

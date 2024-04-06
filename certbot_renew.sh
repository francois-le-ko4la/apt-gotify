#!/bin/sh

URL="https://url:443"
TOKEN="XXXXX"
CERT="/etc/letsencrypt/live/<domain>/fullchain.pem"

MD5_OLD=$(md5sum $CERT | cut -d' ' -f1)
docker start certbot
MD5_NEW=$(md5sum $CERT | cut -d' ' -f1)
INFO=$(cat /var/log/letsencrypt/letsencrypt.log | grep INFO | cut -d: -f6)

TITLE="Certbot: New certificat generated"
PRIO=5
if [ "$MD5_OLD" = "$MD5_NEW" ]; then
	TITLE="Certbot: Keep the existing certificate"
	PRIO=0
fi

curl "$URL/message?token=$TOKEN" -F "title=$TITLE" -F "message=$INFO" -F "priority=$PRIO"

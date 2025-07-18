#!/bin/sh
ARGS="--host 0.0.0.0 --port 8000"
if [ -n "$SSL_KEYFILE" ] && [ -n "$SSL_CERTFILE" ]; then
  ARGS="$ARGS --ssl-keyfile $SSL_KEYFILE --ssl-certfile $SSL_CERTFILE"
fi
exec uvicorn app.main:app $ARGS

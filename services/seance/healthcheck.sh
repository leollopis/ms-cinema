#!/bin/sh
# simple healthcheck used during debugging — returns 0 when service responds
PORT=${PORT:-3000}
if command -v wget >/dev/null 2>&1; then
  wget -qO- "http://127.0.0.1:${PORT}/" >/dev/null 2>&1
  exit $?
fi
if command -v curl >/dev/null 2>&1; then
  curl -fs "http://127.0.0.1:${PORT}/" >/dev/null 2>&1
  exit $?
fi
exit 1

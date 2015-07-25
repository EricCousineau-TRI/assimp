#!/bin/sh

UPSTREAM=$1

if [ -e "${UPSTREAM}" ]; then
 gbp import-orig \
  --filter .gitignore \
  --filter test/ \
  --filter-pristine-tar --pristine-tar \
  --sign-tags \
  ${UPSTREAM}
else
  echo "usage: $0 <upstream.tgz>" 1>&2
  exit 1
fi

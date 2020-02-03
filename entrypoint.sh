#!/bin/sh
set -e
set -x

cd /src/scraperapp && python setup.py bdist_egg
exec python3 /tmp/app/worker.py

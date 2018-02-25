#!/bin/bash

pip install --no-cache-dir -U pip setuptools #wheel
pip install --no-cache-dir uwsgi
pip install --no-cache-dir -r /opt/insta-follow/requirements.txt

exec /usr/local/bin/uwsgi --yaml /opt/insta-follow/uwsgi.yaml

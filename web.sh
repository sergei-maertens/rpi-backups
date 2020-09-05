#!/bin/bash

./env/bin/uwsgi \
    --http :8000 \
    --module monitor.wsgi \
    --static-map /static=./statics \
    --enable-threads \
    --processes 1 \
    --threads 2

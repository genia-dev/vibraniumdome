#!/bin/bash

exec PROMETHEUS_MULTIPROC_DIR=/tmp/ $POETRY_HOME/bin/poetry run gunicorn --bind 0.0.0.0:5001 --threads 4 --workers 4 --preload vibraniumdome_shields.main:app -k gthread
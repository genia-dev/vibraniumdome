#!/bin/bash

PROMETHEUS_MULTIPROC_DIR=/tmp/ exec $POETRY_HOME/bin/poetry run gunicorn --bind 0.0.0.0:5001 --threads 1 --workers 1 --preload vibraniumdome_shields.main:app -k gthread

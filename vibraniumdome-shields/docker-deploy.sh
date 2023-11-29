#!/bin/bash
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t vibraniumdome/vibraniumdome-shields:0.1.0 --push .

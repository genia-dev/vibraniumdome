#!/bin/bash
set -a
source .env.example
set +a
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 \
                    --build-arg DATABASE_URL=${DATABASE_URL} \
                    --build-arg NEXTAUTH_SECRET=${NEXTAUTH_SECRET} \
                    --build-arg NEXTAUTH_URL=${NEXTAUTH_URL} \
                    --build-arg GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID} \
                    --build-arg GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET} \
                    --build-arg OPENSEARCH_JWT_HMAC_SIGNING_KEY=${OPENSEARCH_JWT_HMAC_SIGNING_KEY} \
                    --build-arg OPENSEARCH_DASHBOARD_URL=${OPENSEARCH_DASHBOARD_URL} \
                    --tag=vibraniumdome/vibraniumdome-app:0.1.0 --push .

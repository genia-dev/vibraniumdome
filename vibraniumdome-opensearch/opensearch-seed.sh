#!/bin/bash

check_opensearch() {
    curl -k "https://vibraniumdome-opensearch-node-1:9200/_cluster/health" > /dev/null
    curl -k "https://vibraniumdome-opensearch-node-2:9200/_cluster/health" > /dev/null
}

check_dashboard() {
    curl -fsSL "http://vibraniumdome-opensearch-dashboards:5601" > /dev/null
}

echo "Waiting for OpenSearch to be ready..."
until check_opensearch; do
  sleep 5
done

echo "OpenSearch is ready. Running the seed script..."

status=0
while [ "$status" -ne 200 ]; do
    response=$(curl -vvv -XPUT -k "https://vibraniumdome-opensearch-node-1:9200/_plugins/_security/api/rolesmapping/all_access" \
                    -u 'admin:admin' -H 'Content-Type: application/json' -d '
                    {
                      "backend_roles": ["all_access"],
                      "hosts": [],
                      "users": ["admin"]
                    }
                    ' -w '%{http_code}' -o /dev/null -s)
    
    status=$response
    echo "HTTP Status: $status"

    if [ "$status" -ne 200 ]; then
        echo "Received status $status, retrying in 5 seconds..."
        sleep 5
    fi
done

echo "OpenSearch seeding completed."

echo "Waiting for OpenSearch Dashboard to be ready..."
until check_opensearch; do
  sleep 5
done

sleep 5

echo "OpenSearch Dashboard is ready. Running the seed script..."

status=415
until [ "$status" -ne 415 ]; do
    response=$(curl -vvv -X POST "http://vibraniumdome-opensearch-dashboards:5601/api/saved_objects/_import?overwrite=true" \
                    -H "kbn-xsrf: true" --form "file=@dashboard.ndjson" \
                    -H "osd-xsrf: true" -k -u admin:admin \
                    -w '%{http_code}' -o /dev/null -s)
    status=$response
    echo "HTTP Status: $status"

    if [ "$status" -eq 415 ]; then
        echo "Received status 415, retrying in 5 seconds..."
        sleep 5
    fi
done

echo "OpenSearch Dashboard seeding completed."

echo "Seeding completed."
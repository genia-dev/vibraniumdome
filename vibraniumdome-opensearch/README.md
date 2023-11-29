# vibraniumdome-opensearch

## Usage:

```
git clone git@github.com:genia-dev/vibraniumdome.git
cd vibraniumdome/vibraniumdome-opensearch
poetry install
docker-compose up
```

### After few minutes the OpenSearch will be available, test it works with default creds
```
curl -v -u admin:admin -k https://localhost:9200/_cluster/health
```

### Open browser to OpenSearch Dashboard (creds: admin admin):
```
open http://localhost:5601
```

### Run Client Example
```
poetry run python client_example.py
```

You can check the vibranium index was created succesfully here:

http://localhost:5601/app/opensearch_index_management_dashboards#/indices?from=0&search=&showDataStreams=false&size=20&sortDirection=desc&sortField=index


### create the dashboard
In open search the saved objects can be seen here:
http://localhost:5601/app/management/opensearch-dashboards/objects

saved objects such as index pattern, saved searches, dashboards, visualization widgets etc are required for vibranium dashboard to work

it can be loaded to the index (overrite existing version) running this:

```
curl -X POST "http://localhost:5601/api/saved_objects/_import?overwrite=true" -H "kbn-xsrf: true" --form "file=@dashboard.ndjson" -H "osd-xsrf: true" -k -u admin:admin
```
> [!WARNING]
> Note regarding error: `max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]`
>
> According to the [docs](https://www.elastic.co/guide/en/elasticsearch/reference/8.11/docker.html#_macos_with_docker_for_mac), if you are running the OpenSearch in container, you need to configure the kernel parameter `vm.max_map_count` to: `262144`, as the default is `65530`. In Mac, the suggested solution not working, so the workaround, is to change it once in `privileged` mode, then the future one will be the higher value, the command is:
>
> `docker run --rm --privileged alpine sysctl -w vm.max_map_count=262144`
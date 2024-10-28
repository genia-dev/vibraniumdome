# VibraniumDome Helm Chart

## Prerequisites
[Helm installed](https://helm.sh/docs/helm/helm_install/)

## Install VibraniumDome Helm Chart
**Note:** you can run it locally on [Minikube](https://minikube.sigs.k8s.io/docs/start/). The default resources in Minikube are low, so when start Minikube, provide higher resources, e.g:

```
minikube start --memory 24000 --cpus 10
```

## Create OPENAI_API_KEY in k8s
```
kubectl create secret generic vibraniumdome-shields-secrets --from-literal=OPENAI_API_KEY=$OPENAI_API_KEY
```

```
git clone git@github.com:genia-dev/vibraniumdome.git
cd vibraniumdome
helm install test-release helm
```

## Check system is running
```
kubectl get pods
```

Should show:

```
NAME                                    READY   STATUS    RESTARTS   AGE
vibraniumdome-app-0                     1/1     Running   0          5s
vibraniumdome-app-db-0                  1/1     Running   0          5s
vibraniumdome-opensearch-dashboards-0   1/1     Running   0          5s
vibraniumdome-opensearch-node-1-0       1/1     Running   0          5s
vibraniumdome-opensearch-seeder-rnvm6   1/1     Running   0          5s
vibraniumdome-shields-0                 1/1     Running   0          5s
vibraniumdome-streamlit-app-0           1/1     Running   0          5s
```

When the `vibraniumdome-opensearch-seeder` job STATUS changed from `Running` to `Completed`, you can access the app.

**Note:** In Minikube mode you need to expose the k8s services to your localhost by:

```
kubectl port-forward service/vibraniumdome-app 3000:3000
```

```
kubectl port-forward service/vibraniumdome-opensearch-dashboards 5601:5601
```

```
kubectl port-forward service/vibraniumdome-shields 5001:5001
```

```
kubectl port-forward service/vibraniumdome-streamlit-app 8501:8501
```

Now you can access the application via http://localhost:3000 and the streamlit application via http://localhost:8501 and send llm interactions via http://localhost:5001 .


## Uninstall VibraniumDome Helm Chart
```
helm uninstall test-release
```
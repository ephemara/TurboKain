# K8s

Markscript Kubernetes integration - cluster management, deployments,
services, pods, and observability through kubectl shell dispatch.

---

## apply

Create or update resources from a manifest file.

> run "kubectl apply -f deployment.yaml"

```markscript
# Apply a deployment manifest
push("kubectl apply -f deployment.yaml")
call("run")
```

> run "kubectl apply -f ./manifests/ --recursive"

```markscript
# Apply all manifests in a directory recursively
push("kubectl apply -f ./manifests/ --recursive")
call("run")
```

---

## delete

Delete resources by file, type, or name.

> run "kubectl delete -f deployment.yaml"

```markscript
# Delete resources from a manifest
push("kubectl delete -f deployment.yaml")
call("run")
```

> run "kubectl delete pod web-5d9f7c6b-abc12"

```markscript
# Delete a specific pod
push("kubectl delete pod web-5d9f7c6b-abc12")
call("run")
```

> run "kubectl delete deployment web"

```markscript
# Delete a deployment
push("kubectl delete deployment web")
call("run")
```

---

## get

List resources by type.

> run "kubectl get pods -o wide"

```markscript
# List all pods with node info
push("kubectl get pods -o wide")
call("run")
```

> run "kubectl get all -n production"

```markscript
# List all resources in the production namespace
push("kubectl get all -n production")
call("run")
```

> run "kubectl get nodes"

```markscript
# List cluster nodes
push("kubectl get nodes")
call("run")
```

---

## describe

Show detailed information about a resource.

> run "kubectl describe pod web-5d9f7c6b-abc12"

```markscript
# Describe a specific pod
push("kubectl describe pod web-5d9f7c6b-abc12")
call("run")
```

> run "kubectl describe svc api-gateway"

```markscript
# Describe a service
push("kubectl describe svc api-gateway")
call("run")
```

---

## logs

View pod logs.

> run "kubectl logs web-5d9f7c6b-abc12"

```markscript
# View logs for a single-container pod
push("kubectl logs web-5d9f7c6b-abc12")
call("run")
```

> run "kubectl logs -f deployment/web -c sidecar"

```markscript
# Follow logs from a specific container in a deployment
push("kubectl logs -f deployment/web -c sidecar")
call("run")
```

> run "kubectl logs --tail=20 --since=1h -l app=nginx"

```markscript
# Tail last 20 lines from all pods matching label
push("kubectl logs --tail=20 --since=1h -l app=nginx")
call("run")
```

---

## exec

Execute a command inside a running pod.

> run "kubectl exec -it web-5d9f7c6b-abc12 -- sh"

```markscript
# Open an interactive shell in a pod
push("kubectl exec -it web-5d9f7c6b-abc12 -- sh")
call("run")
```

> run "kubectl exec web-5d9f7c6b-abc12 -- cat /etc/config/app.properties"

```markscript
# Run a command non-interactively
push("kubectl exec web-5d9f7c6b-abc12 -- cat /etc/config/app.properties")
call("run")
```

---

## port_forward

Forward a local port to a pod.

> run "kubectl port-forward svc/postgres 5432:5432"

```markscript
# Forward local port 5432 to postgres service
push("kubectl port-forward svc/postgres 5432:5432")
call("run")
```

> run "kubectl port-forward pod/redis 6379:6379"

```markscript
# Forward to a specific pod
push("kubectl port-forward pod/redis 6379:6379")
call("run")
```

---

## scale

Scale a deployment to a desired replica count.

> run "kubectl scale deployment web --replicas=5"

```markscript
# Scale web deployment to 5 replicas
push("kubectl scale deployment web --replicas=5")
call("run")
```

> run "kubectl scale deployment api --replicas=0"

```markscript
# Scale a deployment down to zero (drain)
push("kubectl scale deployment api --replicas=0")
call("run")
```

---

## rollout

Manage rollout of a deployment (status, history, undo).

> run "kubectl rollout status deployment/web"

```markscript
# Watch rollout status
push("kubectl rollout status deployment/web")
call("run")
```

> run "kubectl rollout history deployment/web"

```markscript
# Show rollout history
push("kubectl rollout history deployment/web")
call("run")
```

> run "kubectl rollout undo deployment/web --to-revision=2"

```markscript
# Rollback to revision 2
push("kubectl rollout undo deployment/web --to-revision=2")
call("run")
```

---

## context

Manage kubectl contexts and namespaces.

> run "kubectl config get-contexts"

```markscript
# List all contexts
push("kubectl config get-contexts")
call("run")
```

> run "kubectl config use-context production"

```markscript
# Switch to the production context
push("kubectl config use-context production")
call("run")
```

> run "kubectl config set-context --current --namespace=staging"

```markscript
# Set the default namespace for current context
push("kubectl config set-context --current --namespace=staging")
call("run")
```

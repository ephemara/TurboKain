# Docker

Markscript Docker integration - container lifecycle, image management,
and Compose orchestration through shell dispatch.

---

## build

Build an image from a Dockerfile.

> run "docker build -t my-app:latest ."

```markscript
# Build image with tag
push("docker build -t my-app:latest .")
call("run")
```

---

## run

Create and start a container from an image.

> run "docker run -d --name web -p 8080:80 nginx:alpine"

```markscript
# Run a detached nginx container
push("docker run -d --name web -p 8080:80 nginx:alpine")
call("run")
```

---

## ps

List running containers.

> run "docker ps -a"

```markscript
# Show all containers (including stopped)
push("docker ps -a")
call("run")
```

---

## stop

Stop one or more running containers gracefully.

> run "docker stop web"

```markscript
# Stop container named 'web'
push("docker stop web")
call("run")
```

---

## rm

Remove one or more containers.

> run "docker rm -f web"

```markscript
# Force-remove container named 'web'
push("docker rm -f web")
call("run")
```

---

## images

List locally available Docker images.

> run "docker images"

```markscript
# List all images
push("docker images")
call("run")
```

> run "docker images --filter reference=nginx"

```markscript
# Filter images matching 'nginx'
push("docker images --filter reference=nginx")
call("run")
```

---

## pull

Pull an image from a registry.

> run "docker pull postgres:16-alpine"

```markscript
# Pull PostgreSQL 16 Alpine image
push("docker pull postgres:16-alpine")
call("run")
```

---

## push

Push an image to a registry.

> run "docker push my-registry.io/app:v1.0"

```markscript
# Push to private registry
push("docker push my-registry.io/app:v1.0")
call("run")
```

---

## compose_up

Start services defined in a Compose file.

> run "docker compose up -d"

```markscript
# Start all services in detached mode
push("docker compose up -d")
call("run")
```

> run "docker compose -f infra/docker-compose.yml up -d"

```markscript
# Start services from a custom compose file
push("docker compose -f infra/docker-compose.yml up -d")
call("run")
```

---

## compose_down

Stop and remove Compose-managed containers.

> run "docker compose down -v"

```markscript
# Stop services and remove volumes
push("docker compose down -v")
call("run")
```

---

## logs

Fetch logs from a container.

> run "docker logs -f --tail 50 web"

```markscript
# Tail last 50 lines of web container logs
push("docker logs -f --tail 50 web")
call("run")
```

---

## exec

Execute a command inside a running container.

> run "docker exec -it web sh"

```markscript
# Open interactive shell in the web container
push("docker exec -it web sh")
call("run")
```

> run "docker exec web cat /etc/nginx/nginx.conf"

```markscript
# Run a command non-interactively
push("docker exec web cat /etc/nginx/nginx.conf")
call("run")
```

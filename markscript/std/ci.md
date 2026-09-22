# CI

Markscript CI/CD integration -- pipeline orchestration, stage management,
artifact handling, and webhook triggers through shell dispatch.

---

## pipeline

Define and trigger a CI pipeline.

> run "pipeline run .github/workflows/ci.yml"

```markscript
# Run a GitHub Actions workflow locally
push("act -W .github/workflows/ci.yml")
call("run")
```

> run "gitlab-ci-local --file .gitlab-ci.yml"

```markscript
# Run a GitLab CI pipeline locally
push("gitlab-ci-local --file .gitlab-ci.yml")
call("run")
```

---

## stage

Run a specific pipeline stage.

> run "act -j build -W .github/workflows/ci.yml"

```markscript
# Run only the 'build' job from a workflow
push("act -j build -W .github/workflows/ci.yml")
call("run")
```

> run "act -j test --rebuild"

```markscript
# Force rebuild and run the 'test' job
push("act -j test --rebuild")
call("run")
```

---

## job

Execute a single CI job.

> run "act -j lint --container-architecture linux/amd64"

```markscript
# Run 'lint' job with architecture override
push("act -j lint --container-architecture linux/amd64")
call("run")
```

---

## artifact

Upload or download CI artifacts.

> run "gh run download <run_id> --name build-logs"

```markscript
# Download named artifact from a GitHub run
push("gh run download 1234567890 --name build-logs")
call("run")
```

> run "gh run download <run_id> --dir ./artifacts"

```markscript
# Download all artifacts to a directory
push("gh run download 1234567890 --dir ./artifacts")
call("run")
```

---

## trigger

Trigger a pipeline via API or webhook.

> run "curl -X POST -H \"Authorization: token $GITHUB_TOKEN\" https://api.github.com/repos/user/repo/dispatches -d '{\"event_type\":\"deploy\",\"client_payload\":{\"env\":\"staging\"}}'"

```markscript
# Trigger a GitHub repository dispatch event
push("curl -X POST -H \"Authorization: token $GITHUB_TOKEN\" https://api.github.com/repos/user/repo/dispatches -d '{\"event_type\":\"deploy\",\"client_payload\":{\"env\":\"staging\"}}'")
call("run")
```

---

## schedule

List or trigger scheduled pipeline runs.

> run "gh workflow run ci.yml --ref main"

```markscript
# Manually trigger a workflow on main branch
push("gh workflow run ci.yml --ref main")
call("run")
```

> run "gh workflow list --all"

```markscript
# List all workflows and their schedules
push("gh workflow list --all")
call("run")
```

---

## webhook

Test or inspect CI webhook endpoints.

> run "curl -X POST -H \"Content-Type: application/json\" -d '{\"ref\":\"refs/heads/main\"}' http://localhost:8080/webhook"

```markscript
# Send a test push event to a local webhook
push("curl -X POST -H \"Content-Type: application/json\" -d '{\"ref\":\"refs/heads/main\"}' http://localhost:8080/webhook")
call("run")
```

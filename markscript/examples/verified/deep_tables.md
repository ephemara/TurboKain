# Deep Tables

Multi-table configuration expressed as markdown tables. Proves table parsing
scales across multiple tables in one file.

## Server Config

| Host        | Port | MaxConn | Timeout |
|-------------|------|---------|---------|
| localhost   | 8080 | 100     | 30      |
| staging     | 9090 | 200     | 60      |
| production  | 443  | 1000    | 120     |

## Database Config

| Name        | Driver  | Pool  | Replicas |
|-------------|---------|-------|----------|
| primary     | postgres| 50    | 0        |
| analytics   | clickhouse| 25  | 2        |
| cache       | redis   | 100   | 3        |

## Feature Flags

| Feature        | Enabled | Rollout | Owner      |
|----------------|---------|---------|------------|
| dark_mode      | 1       | 100     | ui_team    |
| new_parser     | 1       | 25      | lang_team  |
| gpu_export     | 0       | 0       | gpu_team   |

## Thresholds

| Metric          | Warn | Error | Critical |
|-----------------|------|-------|----------|
| cpu_percent     | 80   | 90    | 95       |
| mem_percent     | 75   | 85    | 95       |
| disk_percent    | 80   | 90    | 95       |
| latency_ms      | 100  | 500   | 1000     |

## verify

```markscript
print("deep_tables: 4 tables parsed and loaded")
```

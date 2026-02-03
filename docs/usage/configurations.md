
# Prometheus 

## Retention Configuration

On MacOS the config file is at `/opt/homebrew/etc/prometheus.yml`
On Linux the config file is at ...
On Windows the config file is at ...

Overall:

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
    - targets: ["localhost:9090"]
  - job_name: 'waterlily'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: '/metrics'
```

Set retention to 1 hour when starting Prometheus:

```bash
prometheus --config.file=/opt/homebrew/etc/prometheus.yml \
           --storage.tsdb.retention.time=1h
```
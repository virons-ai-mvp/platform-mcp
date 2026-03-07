# Monitoring MCP Server - Infrastructure Layer

## Overview

External integrations and technical implementations.

## Future Structure

```
infrastructure/
├── __init__.py
├── clients/
│   ├── cloudwatch_client.py    # CloudWatch MCP client
│   ├── prometheus_client.py    # Prometheus MCP client
│   ├── grafana_client.py       # Grafana MCP client
│   └── elasticsearch_client.py # Elasticsearch MCP client
└── repositories/
    └── metrics_repository.py   # Metrics persistence
```

## Upstreams

| Service | Port | Purpose |
|---------|------|---------|
| cloudwatch | 9109 | AWS metrics |
| prometheus | 9110 | Time-series metrics |
| grafana | 9111 | Dashboards & visualization |
| elasticsearch | 9112 | Log aggregation & search |

## Navigation

← [Core Implementation](../)

# MCP Gateway - Infrastructure Layer

## Overview

External integrations: configuration, metrics, HTTP clients.

## Structure

```
infrastructure/
├── __init__.py
├── config.py           # Configuration loader
└── metrics.py          # Prometheus metrics
```

## Key Components

**config.py** - Load services.json
```python
@dataclass
class ServiceConfig:
    name: str
    url: str
    port: int

def load_config(path: str) -> Config:
    with open(path) as f:
        data = json.load(f)
    return Config(services=[ServiceConfig(**s) for s in data["services"]])
```

**metrics.py** - Prometheus metrics
```python
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)
```

## Backend Services

| Service | URL | Port |
|---------|-----|------|
| infrastructure-mcp | http://virons-infrastructure-mcp | 9100 |
| security-mcp | http://virons-security-mcp | 9500 |
| operations-mcp | http://virons-operations-mcp | 9510 |
| monitoring-mcp | http://virons-monitoring-mcp | 9520 |

## Navigation

← [Core Implementation](../)

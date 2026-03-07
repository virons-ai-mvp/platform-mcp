# Infrastructure Layer

Clients for communicating with upstream MCP servers.

## Base Client

### UpstreamClient

Base class with retry logic and circuit breaker.

```python
from virons.monitoring_mcp_server.infrastructure.upstream_client import UpstreamClient

client = UpstreamClient(
    base_url="http://localhost:9109",
    service_name="cloudwatch",
    timeout=5.0
)

response = await client.call_tool(
    tool_name="get_metric_statistics",
    arguments={"metric": "cpu"},
    correlation_id="abc-123"
)
```

**Features:**
- **Retry Logic**: 3 attempts with exponential backoff (2^attempt seconds)
- **Circuit Breaker**: Opens after 5 consecutive failures
- **Correlation ID**: Adds x-correlation-id header to all requests
- **Timeout**: Configurable per-client (default: 5s)

**Circuit Breaker States:**
- Closed: Normal operation
- Open: Fails fast after 5 failures
- Reset: Manual reset via `_failures = 0`

## Upstream Clients

### CloudWatchClient

AWS CloudWatch metrics and alarms.

```python
from virons.monitoring_mcp_server.infrastructure.cloudwatch_client import CloudWatchClient

client = CloudWatchClient("http://localhost:9109")

# Query metrics
datapoints = await client.get_metric_statistics(
    metric_name="CPUUtilization",
    start_time="2026-03-07T00:00:00Z",
    end_time="2026-03-07T01:00:00Z",
    correlation_id="abc-123"
)

# Create alarm
alarm = await client.create_alarm(
    alarm_name="high_cpu",
    metric_name="cpu_usage",
    threshold=80.0,
    comparison_operator="GreaterThanThreshold",
    correlation_id="abc-123"
)
```

**Upstream Port:** 9109

### PrometheusClient

Prometheus time-series metrics.

```python
from virons.monitoring_mcp_server.infrastructure.prometheus_client import PrometheusClient

client = PrometheusClient("http://localhost:9110")

datapoints = await client.query_range(
    query="cpu_usage",
    start_time="2026-03-07T00:00:00Z",
    end_time="2026-03-07T01:00:00Z",
    correlation_id="abc-123"
)
```

**Upstream Port:** 9110

### GrafanaClient

Grafana dashboard creation.

```python
from virons.monitoring_mcp_server.infrastructure.grafana_client import GrafanaClient

client = GrafanaClient("http://localhost:9111")

dashboard = await client.create_dashboard(
    title="System Overview",
    panels=[
        {"title": "CPU", "targets": [{"expr": "cpu_usage"}], "type": "graph"}
    ],
    correlation_id="abc-123"
)
```

**Upstream Port:** 9111

### ElasticsearchClient

Elasticsearch log search.

```python
from virons.monitoring_mcp_server.infrastructure.elasticsearch_client import ElasticsearchClient

client = ElasticsearchClient("http://localhost:9112")

logs = await client.search(
    query="error",
    start_time="2026-03-07T00:00:00Z",
    end_time="2026-03-07T01:00:00Z",
    level="ERROR",
    size=100,
    correlation_id="abc-123"
)
```

**Upstream Port:** 9112

## Error Handling

All clients handle:
- **Connection errors**: Logged and retried
- **Timeout errors**: Logged and retried
- **Circuit breaker open**: Fails fast with error message
- **Invalid responses**: Logged and raised as exceptions

## Configuration

Set upstream URLs via environment variables:

```bash
export CLOUDWATCH_URL=http://cloudwatch:9109
export PROMETHEUS_URL=http://prometheus:9110
export GRAFANA_URL=http://grafana:9111
export ELASTICSEARCH_URL=http://elasticsearch:9112
```

## Testing

```bash
pytest tests/infrastructure/ -v
```

Infrastructure clients are tested with mocked HTTP responses.

## Upstream Integration

See [UPSTREAM_INTEGRATION.md](../UPSTREAM_INTEGRATION.md) for:
- Mock upstream servers
- Real upstream deployment
- Docker Compose setup
- Verification steps

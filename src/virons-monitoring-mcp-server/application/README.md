# Application Layer

Orchestration services that coordinate domain entities and infrastructure clients.

## Services

### MetricsService

Routes metric queries to CloudWatch or Prometheus based on source.

```python
from virons.monitoring_mcp_server.application.metrics_service import MetricsService

service = MetricsService()
datapoints = await service.query_metrics(
    metric_name="CPUUtilization",
    start_time="2026-03-07T00:00:00Z",
    end_time="2026-03-07T01:00:00Z",
    source="cloudwatch",
    correlation_id="abc-123"
)
```

**Responsibilities:**
- Route to correct upstream (CloudWatch/Prometheus)
- Convert domain entities to infrastructure DTOs
- Handle errors and logging
- Propagate correlation IDs

### AlertService

Creates alert rules in CloudWatch.

```python
from virons.monitoring_mcp_server.application.alert_service import AlertService

service = AlertService()
result = await service.create_alert(
    name="high_cpu",
    metric="cpu_usage",
    threshold=80.0,
    comparison="gt",
    correlation_id="abc-123"
)
```

**Responsibilities:**
- Validate alert configuration using domain logic
- Create alarms in CloudWatch
- Log alert creation for audit trail

### DashboardService

Creates Grafana dashboards with panels.

```python
from virons.monitoring_mcp_server.application.dashboard_service import DashboardService

service = DashboardService()
result = await service.create_dashboard(
    name="System Overview",
    panels=[
        {"title": "CPU", "query": "cpu_usage", "type": "graph"},
        {"title": "Memory", "query": "memory_usage", "type": "stat"}
    ],
    correlation_id="abc-123"
)
```

**Responsibilities:**
- Convert panel dicts to domain Panel value objects
- Validate panel types (graph, stat, table)
- Create dashboard in Grafana

### LogService

Searches logs in Elasticsearch.

```python
from virons.monitoring_mcp_server.application.log_service import LogService

service = LogService()
logs = await service.search_logs(
    query="error",
    start_time="2026-03-07T00:00:00Z",
    end_time="2026-03-07T01:00:00Z",
    level="ERROR",
    size=50,
    correlation_id="abc-123"
)
```

**Responsibilities:**
- Build log queries using domain LogQuery
- Execute search in Elasticsearch
- Format results as LogEntry entities

## Pattern

All services follow the same pattern:

1. **Accept domain parameters** from server layer
2. **Create domain entities/value objects** for validation
3. **Call infrastructure clients** with validated data
4. **Handle errors** and log operations
5. **Return formatted results** to server layer

## Testing

```bash
pytest tests/application/ -v
```

All services are tested with mocked infrastructure clients.

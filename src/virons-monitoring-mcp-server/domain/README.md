# Domain Layer

Core business entities and value objects with validation logic.

## Entities

### Metric

Represents a time-series metric datapoint.

```python
from virons.monitoring_mcp_server.domain.metric import Metric

metric = Metric(
    name="CPUUtilization",
    value=75.5,
    timestamp="2026-03-07T10:00:00Z",
    labels={"instance": "i-123"}
)
```

**Validation:**
- `name` is required
- `value` is required
- `timestamp` defaults to current time

### Alert

Represents an alert rule with evaluation logic.

```python
from virons.monitoring_mcp_server.domain.alert import Alert

alert = Alert(
    name="high_cpu",
    metric="cpu_usage",
    threshold=80.0,
    comparison="gt"
)

# Business logic
is_triggered = alert.evaluate(current_value=85.0)  # True
```

**Validation:**
- `comparison` must be "gt", "lt", or "eq"
- `threshold` is required

**Business Logic:**
- `evaluate(value)`: Returns True if alert should trigger

### Dashboard

Represents a Grafana dashboard with panels.

```python
from virons.monitoring_mcp_server.domain.dashboard import Dashboard, Panel

dashboard = Dashboard(name="System Overview")
dashboard.add_panel(Panel(title="CPU", query="cpu_usage", type="graph"))
dashboard.add_panel(Panel(title="Memory", query="memory_usage", type="stat"))

count = dashboard.panel_count()  # 2
```

**Validation:**
- `name` is required
- Panel `type` must be "graph", "stat", or "table"

**Business Logic:**
- `add_panel(panel)`: Adds panel to dashboard
- `panel_count()`: Returns number of panels

### LogEntry

Represents a log entry from Elasticsearch.

```python
from virons.monitoring_mcp_server.domain.log_entry import LogEntry

log = LogEntry(
    timestamp="2026-03-07T10:00:00Z",
    message="Application error",
    level="ERROR",
    labels={"app": "api", "env": "prod"}
)
```

**Validation:**
- `level` must be "INFO", "WARN", "ERROR", or "DEBUG"
- `message` is required

## Value Objects

### MetricQuery

Query parameters for metric retrieval.

```python
from virons.monitoring_mcp_server.domain.metric import MetricQuery

query = MetricQuery(
    metric_name="CPUUtilization",
    start_time="2026-03-07T00:00:00Z",
    end_time="2026-03-07T01:00:00Z",
    source="cloudwatch"
)
```

**Validation:**
- `source` must be "cloudwatch" or "prometheus"
- Defaults to "cloudwatch"

### Panel

Dashboard panel configuration.

```python
from virons.monitoring_mcp_server.domain.dashboard import Panel

panel = Panel(
    title="CPU Usage",
    query="cpu_usage",
    type="graph"
)
```

**Validation:**
- `type` must be "graph", "stat", or "table"

### LogQuery

Query parameters for log search.

```python
from virons.monitoring_mcp_server.domain.log_entry import LogQuery

query = LogQuery(
    query="error",
    start_time="2026-03-07T00:00:00Z",
    end_time="2026-03-07T01:00:00Z",
    level="ERROR",
    size=100
)
```

**Validation:**
- `size` must be between 1 and 10000
- `level` must be valid log level if provided

## Design Principles

1. **Immutability**: Value objects are immutable
2. **Validation**: All validation happens in domain layer
3. **Business Logic**: Domain entities contain business rules
4. **No Dependencies**: Domain layer has no external dependencies

## Testing

```bash
pytest tests/domain/ -v
```

All domain entities are tested independently without mocks.

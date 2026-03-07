# Monitoring MCP Server - Implementation Plan

## Overview

Implement 4 orchestrator tools connecting to 4 upstream MCP servers for metrics, logs, dashboards, and alerts.

**Timeline:** 2-3 hours  
**Approach:** Minimal implementation, upstream-first

## Upstream MCP Servers

### Required Upstreams

| Server | Port | Purpose | Status | Priority |
|--------|------|---------|--------|----------|
| CloudWatch | 9109 | AWS metrics & logs | ❌ Not running | P0 |
| Prometheus | 9110 | Prometheus metrics | ❌ Not running | P0 |
| Grafana | 9111 | Dashboard creation | ❌ Not running | P1 |
| Elasticsearch | 9112 | Log search | ❌ Not running | P1 |

### Decision Point

**Option A:** Implement with real upstream servers (4-6 hours)
- Requires setting up 4 additional MCP servers
- Full integration testing needed
- Production-ready

**Option B:** Implement with mock/stub upstreams (1-2 hours)
- Faster development
- Can test orchestration logic
- Replace with real upstreams later

**Recommendation:** Option B for MVP, then Option A

## Implementation Checklist

### Phase 1: Infrastructure (30 min)

- [ ] Create `virons/monitoring_mcp_server/infrastructure/upstream_client.py`
  - [ ] `UpstreamClient` base class
  - [ ] HTTP client with retries
  - [ ] Circuit breaker pattern
  - [ ] Timeout handling

- [ ] Create `virons/monitoring_mcp_server/infrastructure/cloudwatch_client.py`
  - [ ] `query_metrics()` method
  - [ ] `search_logs()` method
  - [ ] `create_alarm()` method

- [ ] Create `virons/monitoring_mcp_server/infrastructure/prometheus_client.py`
  - [ ] `query_range()` method
  - [ ] `query_instant()` method

- [ ] Create `virons/monitoring_mcp_server/infrastructure/grafana_client.py`
  - [ ] `create_dashboard()` method
  - [ ] `update_dashboard()` method

- [ ] Create `virons/monitoring_mcp_server/infrastructure/elasticsearch_client.py`
  - [ ] `search()` method
  - [ ] `aggregate()` method

### Phase 2: Domain Logic (20 min)

- [ ] Create `virons/monitoring_mcp_server/domain/metric.py`
  - [ ] `Metric` entity (name, value, timestamp, labels)
  - [ ] `MetricQuery` value object

- [ ] Create `virons/monitoring_mcp_server/domain/alert.py`
  - [ ] `Alert` entity (name, metric, threshold, comparison)
  - [ ] `AlertRule` value object

- [ ] Create `virons/monitoring_mcp_server/domain/dashboard.py`
  - [ ] `Dashboard` entity (name, panels)
  - [ ] `Panel` value object

- [ ] Create `virons/monitoring_mcp_server/domain/log_entry.py`
  - [ ] `LogEntry` entity (timestamp, message, level, source)
  - [ ] `LogQuery` value object

### Phase 3: Application Services (30 min)

- [ ] Create `virons/monitoring_mcp_server/application/metrics_service.py`
  - [ ] `query_metrics()` - Route to CloudWatch or Prometheus
  - [ ] Aggregate results from multiple sources
  - [ ] Handle errors and fallbacks

- [ ] Create `virons/monitoring_mcp_server/application/alert_service.py`
  - [ ] `create_alert()` - Create in CloudWatch or Prometheus
  - [ ] Validate alert rules
  - [ ] Audit trail integration

- [ ] Create `virons/monitoring_mcp_server/application/dashboard_service.py`
  - [ ] `create_dashboard()` - Create in Grafana
  - [ ] Validate panel configurations
  - [ ] Audit trail integration

- [ ] Create `virons/monitoring_mcp_server/application/log_service.py`
  - [ ] `search_logs()` - Search in Elasticsearch or CloudWatch
  - [ ] Parse and normalize results
  - [ ] Handle pagination

### Phase 4: Update Server Tools (20 min)

- [ ] Update `server.py::query_metrics()`
  - [ ] Replace TODO with `MetricsService.query_metrics()`
  - [ ] Add error handling
  - [ ] Add response formatting

- [ ] Update `server.py::create_alert()`
  - [ ] Replace TODO with `AlertService.create_alert()`
  - [ ] Keep audit trail
  - [ ] Add validation

- [ ] Update `server.py::create_dashboard()`
  - [ ] Replace TODO with `DashboardService.create_dashboard()`
  - [ ] Keep audit trail
  - [ ] Add validation

- [ ] Update `server.py::search_logs()`
  - [ ] Replace TODO with `LogService.search_logs()`
  - [ ] Add error handling
  - [ ] Add pagination

### Phase 5: Testing (30 min)

- [ ] Create `tests/infrastructure/test_upstream_client.py`
  - [ ] Test retry logic
  - [ ] Test circuit breaker
  - [ ] Test timeout handling

- [ ] Create `tests/application/test_metrics_service.py`
  - [ ] Test CloudWatch routing
  - [ ] Test Prometheus routing
  - [ ] Test error handling

- [ ] Create `tests/application/test_alert_service.py`
  - [ ] Test alert creation
  - [ ] Test validation
  - [ ] Test audit trail

- [ ] Create `tests/application/test_dashboard_service.py`
  - [ ] Test dashboard creation
  - [ ] Test panel validation

- [ ] Create `tests/application/test_log_service.py`
  - [ ] Test log search
  - [ ] Test result normalization

- [ ] Integration tests
  - [ ] Test all 4 tools end-to-end
  - [ ] Test with mock upstreams
  - [ ] Test error scenarios

### Phase 6: Documentation (20 min)

- [ ] Update `README.md`
  - [ ] Remove "TODO" mentions
  - [ ] Add implementation status
  - [ ] Add upstream requirements

- [ ] Update layer READMEs
  - [ ] `application/README.md` - Document services
  - [ ] `domain/README.md` - Document entities
  - [ ] `infrastructure/README.md` - Document clients

- [ ] Update `tool_metadata.py`
  - [ ] Add real examples
  - [ ] Add upstream_service field
  - [ ] Add error scenarios

## Implementation Order

### Iteration 1: Metrics (45 min)
1. Infrastructure: `UpstreamClient`, `CloudWatchClient`, `PrometheusClient`
2. Domain: `Metric`, `MetricQuery`
3. Application: `MetricsService`
4. Server: Update `query_metrics()`
5. Tests: Basic integration test

### Iteration 2: Alerts (30 min)
1. Domain: `Alert`, `AlertRule`
2. Application: `AlertService`
3. Server: Update `create_alert()`
4. Tests: Alert creation test

### Iteration 3: Dashboards (30 min)
1. Infrastructure: `GrafanaClient`
2. Domain: `Dashboard`, `Panel`
3. Application: `DashboardService`
4. Server: Update `create_dashboard()`
5. Tests: Dashboard creation test

### Iteration 4: Logs (30 min)
1. Infrastructure: `ElasticsearchClient`
2. Domain: `LogEntry`, `LogQuery`
3. Application: `LogService`
4. Server: Update `search_logs()`
5. Tests: Log search test

## Mock Upstream Strategy

For MVP without real upstreams:

```python
# infrastructure/mock_upstream.py
class MockUpstreamClient:
    async def call_tool(self, tool_name: str, params: dict) -> dict:
        # Return realistic mock data
        if tool_name == "query_metrics":
            return {"datapoints": [{"timestamp": "...", "value": 42.0}]}
        # ... etc
```

Enable with environment variable:
```bash
MOCK_UPSTREAMS=true python -m virons.monitoring_mcp_server.server --transport api
```

## Validation Criteria

### Functional
- [ ] All 4 tools return valid responses
- [ ] Error handling works (upstream down, timeout, invalid params)
- [ ] Audit trails created for write operations
- [ ] Correlation IDs propagated to upstreams

### Non-Functional
- [ ] Response time < 2s for queries
- [ ] Response time < 5s for writes
- [ ] Circuit breaker opens after 5 failures
- [ ] Retries 3 times with exponential backoff

### Documentation
- [ ] All TODOs removed from code
- [ ] READMEs updated with implementation details
- [ ] Examples work with mock upstreams
- [ ] Pre-push hook passes

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Upstream servers not available | High | Use mock upstreams for MVP |
| Different upstream protocols | Medium | Abstract with UpstreamClient |
| Slow upstream responses | Medium | Add timeouts and circuit breakers |
| Complex error handling | Low | Start simple, iterate |

## Success Metrics

- [ ] 4/4 tools implemented
- [ ] 0 TODO comments in server.py
- [ ] Test coverage > 80%
- [ ] Pre-push hook passes
- [ ] Documentation complete

## Next Steps After Completion

1. Deploy real upstream MCP servers
2. Replace mock clients with real implementations
3. Add caching layer for metrics
4. Add aggregation across multiple sources
5. Add advanced features (anomaly detection, forecasting)

---

**Estimated Total Time:** 2-3 hours (with mocks) or 4-6 hours (with real upstreams)

**Start with:** Phase 1 (Infrastructure) → Iteration 1 (Metrics)

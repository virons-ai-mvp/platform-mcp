# Upstream Integration Guide

## Current State

Monitoring MCP is **ready** but upstream servers are **not running**:

| Upstream | Port | Status | Purpose |
|----------|------|--------|---------|
| CloudWatch | 9109 | ❌ Not running | AWS metrics & logs |
| Prometheus | 9110 | ❌ Not running | Prometheus metrics |
| Grafana | 9111 | ❌ Not running | Dashboard creation |
| Elasticsearch | 9112 | ❌ Not running | Log search |

## Integration Options

### Option 1: Mock Upstreams (Fast - 15 min)

For testing without real servers.

**Step 1:** Create mock server

```bash
cd src/virons-monitoring-mcp-server
mkdir -p mock_upstreams
cat > mock_upstreams/mock_server.py << 'EOF'
"""Mock upstream MCP servers for testing."""
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/tools/get_metric_statistics")
async def mock_cloudwatch_metrics(request: dict):
    return {
        "datapoints": [
            {"Timestamp": "2026-03-07T10:00:00Z", "Average": 75.5},
            {"Timestamp": "2026-03-07T10:05:00Z", "Average": 80.2}
        ]
    }

@app.post("/tools/put_metric_alarm")
async def mock_cloudwatch_alarm(request: dict):
    return {"alarm_arn": f"arn:aws:cloudwatch:alarm:{request['alarm_name']}"}

@app.post("/tools/query_range")
async def mock_prometheus_query(request: dict):
    return {
        "data": {
            "result": [{
                "metric": {"__name__": request["query"], "job": "node"},
                "values": [[1709809200, "75.5"], [1709809500, "80.2"]]
            }]
        }
    }

@app.post("/tools/create_dashboard")
async def mock_grafana_dashboard(request: dict):
    return {"id": "abc123", "url": f"/d/{request['title']}"}

@app.post("/tools/search")
async def mock_elasticsearch_search(request: dict):
    return {
        "hits": [{
            "_source": {
                "timestamp": "2026-03-07T10:00:00Z",
                "message": "Application error",
                "level": "ERROR",
                "labels": {"app": "api"}
            }
        }]
    }

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9109
    print(f"Mock upstream on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
EOF
```

**Step 2:** Start mock servers

```bash
# Terminal 1: CloudWatch mock
python3 mock_upstreams/mock_server.py 9109

# Terminal 2: Prometheus mock
python3 mock_upstreams/mock_server.py 9110

# Terminal 3: Grafana mock
python3 mock_upstreams/mock_server.py 9111

# Terminal 4: Elasticsearch mock
python3 mock_upstreams/mock_server.py 9112
```

**Step 3:** Test integration

```bash
# Start monitoring MCP
python3 -m virons.monitoring_mcp_server.server --transport api

# Test query_metrics
curl -X POST http://localhost:9520/tools/query_metrics \
  -H "Content-Type: application/json" \
  -d '{
    "metric_name": "CPUUtilization",
    "start_time": "2026-03-07T00:00:00Z",
    "end_time": "2026-03-07T01:00:00Z",
    "source": "cloudwatch"
  }' | jq

# Test create_alert
curl -X POST http://localhost:9520/tools/create_alert \
  -H "Content-Type: application/json" \
  -d '{
    "name": "high_cpu",
    "metric": "cpu_usage",
    "threshold": 80.0,
    "comparison": "gt"
  }' | jq
```

---

### Option 2: Real MCP Servers (Production - 2-4 hours)

Deploy actual upstream MCP servers.

#### 2.1 CloudWatch MCP Server

```bash
# Clone AWS MCP server
git clone https://github.com/aws/aws-mcp-server
cd aws-mcp-server

# Configure
cat > config.json << EOF
{
  "region": "us-east-1",
  "services": ["cloudwatch"]
}
EOF

# Run
npm install
npm start -- --port 9109
```

#### 2.2 Prometheus MCP Server

```bash
# Use existing Docker image
docker run -d \
  --name prometheus-mcp \
  -p 9110:9110 \
  -e PROMETHEUS_URL=http://prometheus:9090 \
  ghcr.io/pab1it0/prometheus-mcp-server
```

#### 2.3 Grafana MCP Server

```bash
# Create Grafana MCP wrapper
mkdir grafana-mcp-server
cd grafana-mcp-server

cat > server.py << 'EOF'
from fastapi import FastAPI
import httpx
import uvicorn

app = FastAPI()
GRAFANA_URL = "http://localhost:3000"
GRAFANA_TOKEN = "your-api-token"

@app.post("/tools/create_dashboard")
async def create_dashboard(request: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GRAFANA_URL}/api/dashboards/db",
            headers={"Authorization": f"Bearer {GRAFANA_TOKEN}"},
            json={"dashboard": request, "overwrite": False}
        )
        return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9111)
EOF

python3 server.py
```

#### 2.4 Elasticsearch MCP Server

```bash
# Create Elasticsearch MCP wrapper
mkdir elasticsearch-mcp-server
cd elasticsearch-mcp-server

cat > server.py << 'EOF'
from fastapi import FastAPI
from elasticsearch import AsyncElasticsearch
import uvicorn

app = FastAPI()
es = AsyncElasticsearch(["http://localhost:9200"])

@app.post("/tools/search")
async def search(request: dict):
    result = await es.search(
        index="logs-*",
        body={
            "query": {"match": {"message": request["query"]}},
            "size": request.get("size", 100)
        }
    )
    return {"hits": result["hits"]["hits"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9112)
EOF

pip install elasticsearch
python3 server.py
```

---

### Option 3: Docker Compose (Recommended - 30 min)

Add upstreams to docker-compose.yml:

```yaml
# Add to platform-mcp/docker-compose.yml

services:
  # Existing services...
  
  # Mock upstreams for testing
  mock-cloudwatch:
    build:
      context: ./src/virons-monitoring-mcp-server/mock_upstreams
    ports:
      - "9109:9109"
    environment:
      - PORT=9109
    networks:
      - virons-network
  
  mock-prometheus:
    build:
      context: ./src/virons-monitoring-mcp-server/mock_upstreams
    ports:
      - "9110:9110"
    environment:
      - PORT=9110
    networks:
      - virons-network
  
  mock-grafana:
    build:
      context: ./src/virons-monitoring-mcp-server/mock_upstreams
    ports:
      - "9111:9111"
    environment:
      - PORT=9111
    networks:
      - virons-network
  
  mock-elasticsearch:
    build:
      context: ./src/virons-monitoring-mcp-server/mock_upstreams
    ports:
      - "9112:9112"
    environment:
      - PORT=9112
    networks:
      - virons-network
```

**Dockerfile for mocks:**

```dockerfile
# src/virons-monitoring-mcp-server/mock_upstreams/Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY mock_server.py .

RUN pip install fastapi uvicorn

CMD ["python", "mock_server.py"]
```

**Start everything:**

```bash
docker-compose up -d
```

---

## Configuration

Update upstream URLs if needed:

```python
# virons/monitoring_mcp_server/application/metrics_service.py
class MetricsService:
    def __init__(self):
        # Use environment variables for flexibility
        cloudwatch_url = os.getenv("CLOUDWATCH_URL", "http://localhost:9109")
        prometheus_url = os.getenv("PROMETHEUS_URL", "http://localhost:9110")
        
        self.cloudwatch = CloudWatchClient(cloudwatch_url)
        self.prometheus = PrometheusClient(prometheus_url)
```

**Environment variables:**

```bash
export CLOUDWATCH_URL=http://mock-cloudwatch:9109
export PROMETHEUS_URL=http://mock-prometheus:9110
export GRAFANA_URL=http://mock-grafana:9111
export ELASTICSEARCH_URL=http://mock-elasticsearch:9112
```

---

## Verification

**Test all 4 tools:**

```bash
# 1. Query metrics
curl -X POST http://localhost:9520/tools/query_metrics \
  -H "Content-Type: application/json" \
  -d '{"metric_name": "cpu", "start_time": "2026-03-07T00:00:00Z", "end_time": "2026-03-07T01:00:00Z", "source": "cloudwatch"}' | jq

# 2. Create alert
curl -X POST http://localhost:9520/tools/create_alert \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "metric": "cpu", "threshold": 80, "comparison": "gt"}' | jq

# 3. Create dashboard
curl -X POST http://localhost:9520/tools/create_dashboard \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "panels": [{"title": "CPU", "query": "cpu", "type": "graph"}]}' | jq

# 4. Search logs
curl -X POST http://localhost:9520/tools/search_logs \
  -H "Content-Type: application/json" \
  -d '{"query": "error", "start_time": "2026-03-07T00:00:00Z", "end_time": "2026-03-07T01:00:00Z"}' | jq
```

**Expected:** All 4 should return data (not empty arrays)

---

## Troubleshooting

### Connection Refused

```bash
# Check upstream is running
curl http://localhost:9109/health

# Check from monitoring container
docker exec virons-monitoring-mcp curl http://mock-cloudwatch:9109/health
```

### Circuit Breaker Open

```python
# Reset circuit breaker
service.cloudwatch._failures = 0
service.cloudwatch._circuit_open = False
```

### Timeout Errors

```python
# Increase timeout in client initialization
self.cloudwatch = CloudWatchClient("http://localhost:9109", timeout=10.0)
```

---

## Recommendation

**For immediate testing:** Use Option 1 (Mock Upstreams)
**For production:** Use Option 2 (Real MCP Servers)
**For development:** Use Option 3 (Docker Compose)

Start with mocks, validate integration, then swap to real servers.

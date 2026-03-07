# MCP Server Standard Architecture

## Gateway Pattern (Reference Implementation)

All MCP servers MUST follow the gateway's architecture:

### 1. Middleware Stack
```python
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Rate limiting per client IP

@app.middleware("http")
async def correlation_id(request: Request, call_next):
    # x-correlation-id header propagation

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    # Prometheus metrics collection
```

### 2. HTTP Status Codes (Comprehensive)
```python
responses={
    200: {"description": "Success"},
    400: {"description": "Invalid request body"},
    401: {"description": "Authentication required"},
    404: {"description": "Tool not found"},
    500: {"description": "Internal server error"},
    502: {"description": "Bad gateway - upstream service failed"},
    503: {"description": "Service unavailable"},
}
```

### 3. Health Endpoints
```python
@app.get("/health")  # Liveness - is process alive?
async def health():
    return {"status": "healthy"}

@app.get("/ready")   # Readiness - can accept traffic?
async def ready():
    # Check upstream dependencies
    return {"status": "ready", "upstreams": {...}}
```

### 4. Tool Discovery
```python
@app.get("/tools")
async def list_tools():
    """Return enriched tool metadata with examples."""
    return {"tools": [...], "count": N}
```

### 5. Tool Execution
```python
@app.post("/tools/{tool_name}")
async def execute_tool(tool_name: str, request: Request):
    # Auth check
    # JSON validation
    # Route to MCP tool
    # Error handling with proper status codes
```

### 6. Metrics Endpoint
```python
@app.get("/metrics")
async def metrics():
    """Prometheus metrics."""
    return PlainTextResponse(generate_latest(registry))
```

## Required Changes for All Servers

### Infrastructure-MCP ✅ (Partially Done)
- ✅ Has /health endpoint
- ✅ Has /tools endpoint
- ❌ Missing middleware (rate limit, correlation ID, metrics)
- ❌ Missing comprehensive HTTP status codes
- ❌ Missing /ready endpoint
- ❌ Missing /metrics endpoint

### Security-MCP ⚠️
- ✅ Has /health endpoint
- ✅ Has /tools endpoint
- ❌ Missing middleware
- ❌ Missing comprehensive HTTP status codes
- ❌ Missing /ready endpoint
- ❌ Missing /metrics endpoint

### Operations-MCP ⚠️
- ✅ Has /health endpoint
- ✅ Has /tools endpoint
- ❌ Missing middleware
- ❌ Missing comprehensive HTTP status codes
- ❌ Missing /ready endpoint
- ❌ Missing /metrics endpoint

### Monitoring-MCP ⚠️
- ✅ Has /health endpoint
- ✅ Has /tools endpoint
- ❌ Missing middleware
- ❌ Missing comprehensive HTTP status codes
- ❌ Missing /ready endpoint
- ❌ Missing /metrics endpoint

## Implementation Priority

1. **Metrics middleware** - Essential for observability
2. **Correlation ID** - Essential for distributed tracing
3. **Rate limiting** - Essential for production stability
4. **/ready endpoint** - Essential for K8s readiness probes
5. **/metrics endpoint** - Essential for Prometheus scraping
6. **Comprehensive HTTP status codes** - Essential for API clarity

## Minimal Implementation

```python
from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest
import time
import uuid

# Metrics
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
http_request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])

app = FastAPI(title="Virons X MCP Server", version="1.0.0")

@app.middleware("http")
async def correlation_id(request: Request, call_next):
    cid = request.headers.get("x-correlation-id") or str(uuid.uuid4())
    request.state.correlation_id = cid
    response = await call_next(request)
    response.headers["x-correlation-id"] = cid
    return response

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.monotonic()
    response = await call_next(request)
    duration = time.monotonic() - start
    http_requests_total.labels(request.method, request.url.path, str(response.status_code)).inc()
    http_request_duration.labels(request.method, request.url.path).observe(duration)
    return response

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    # Check upstreams if any
    return {"status": "ready"}

@app.get("/metrics")
async def metrics():
    from prometheus_client import generate_latest, REGISTRY
    return PlainTextResponse(generate_latest(REGISTRY))
```

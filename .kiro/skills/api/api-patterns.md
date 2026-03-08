# API Patterns

**Name**: api-patterns
**Description**: JWT/Cognito auth, Redis rate limiting, RFC 7807 errors, cursor pagination, audit logging.
**Namespace**: api
**User-invocable**: false

## JWT Validation — AWS Cognito

```go
import (
    "github.com/lestrrat-go/jwx/v2/jwk"
    "github.com/lestrrat-go/jwx/v2/jwt"
)

const JWKSUrl = "https://cognito-idp.eu-central-1.amazonaws.com/{pool-id}/.well-known/jwks.json"

func NewAuthMiddleware(jwksURL string) gin.HandlerFunc {
    cache := jwk.NewCache(context.Background())
    cache.Register(jwksURL, jwk.WithMinRefreshInterval(15*time.Minute))

    return func(c *gin.Context) {
        tokenStr := strings.TrimPrefix(c.GetHeader("Authorization"), "Bearer ")
        keySet, _ := cache.Get(context.Background(), jwksURL)
        token, err := jwt.Parse([]byte(tokenStr), jwt.WithKeySet(keySet))
        if err != nil {
            c.AbortWithStatusJSON(401, Problem{
                Type:   "https://virons.ai/errors/unauthorized",
                Title:  "Unauthorized",
                Status: 401,
                Detail: "Invalid or expired token",
            })
            return
        }
        c.Set("user_id", token.Subject())
        c.Next()
    }
}
```

## Rate Limiting — Redis Token Bucket

```go
const (
    RateLimit  = 100
    RateWindow = time.Minute
)

func RateLimitMiddleware(rdb *redis.Client) gin.HandlerFunc {
    return func(c *gin.Context) {
        userID := c.GetString("user_id")
        key := "rate_limit:" + userID

        count, _ := rdb.Incr(c, key).Result()
        if count == 1 {
            rdb.Expire(c, key, RateWindow)
        }
        if count > RateLimit {
            c.AbortWithStatusJSON(429, Problem{
                Type:   "https://virons.ai/errors/rate-limit-exceeded",
                Title:  "Too Many Requests",
                Status: 429,
            })
            return
        }
        c.Next()
    }
}
```

## RFC 7807 Problem Details

```go
type Problem struct {
    Type     string `json:"type"`
    Title    string `json:"title"`
    Status   int    `json:"status"`
    Detail   string `json:"detail"`
    Instance string `json:"instance,omitempty"`
}
```

## 100% Audit Logging (GDPR/DORA)

```go
func AuditMiddleware(logger zerolog.Logger) gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        requestID := c.GetHeader("X-Request-ID")
        if requestID == "" {
            requestID = uuid.New().String()
            c.Header("X-Request-ID", requestID)
        }
        c.Next()
        logger.Info().
            Str("request_id", requestID).
            Str("user_id", c.GetString("user_id")).
            Str("method", c.Request.Method).
            Str("path", c.Request.URL.Path).
            Int("status", c.Writer.Status()).
            Dur("duration_ms", time.Since(start)).
            Msg("request")
    }
}
```

# Expert Kubernetes Engineer Agent
**Version**: 1.0.0
**Role**: Kubernetes Architecture & EKS Management
**Stack**: EKS, Helm, Kustomize, ArgoCD
**Risk Level**: CRITICAL (0.95)

## Purpose
Design and manage Kubernetes infrastructure for Virons AI platform (future migration from ECS to EKS).

## Current State
Virons currently uses **ECS Fargate**. This agent provides guidance for future EKS migration.

## EKS Architecture (Future)

### Cluster Design
```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: virons-demo
  region: eu-central-1
  version: "1.29"

vpc:
  id: vpc-xxx
  subnets:
    private:
      eu-central-1a: { id: subnet-xxx }
      eu-central-1b: { id: subnet-xxx }
      eu-central-1c: { id: subnet-xxx }

managedNodeGroups:
  - name: virons-workers
    instanceType: t4g.medium
    desiredCapacity: 3
    minSize: 2
    maxSize: 10
    privateNetworking: true
    iam:
      withAddonPolicies:
        ebs: true
        efs: true
        albIngress: true
    tags:
      Environment: demo
      Project: Virons
```

### Namespace Strategy
```yaml
# Namespaces
apiVersion: v1
kind: Namespace
metadata:
  name: virons-api
  labels:
    environment: demo
---
apiVersion: v1
kind: Namespace
metadata:
  name: virons-ai
---
apiVersion: v1
kind: Namespace
metadata:
  name: virons-data
```

## Application Deployment

### Deployment Manifest
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  namespace: virons-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      serviceAccountName: api-gateway-sa
      containers:
      - name: api
        image: 412179655775.dkr.ecr.eu-central-1.amazonaws.com/virons-api:latest
        ports:
        - containerPort: 8080
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: host
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service & Ingress
```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
  namespace: virons-api
spec:
  selector:
    app: api-gateway
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: virons-ingress
  namespace: virons-api
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:eu-central-1:xxx
spec:
  ingressClassName: alb
  rules:
  - host: api.virons.io
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-gateway
            port:
              number: 80
```

## Security

### RBAC
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: api-deployer
  namespace: virons-api
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "update", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: api-deployer-binding
  namespace: virons-api
subjects:
- kind: ServiceAccount
  name: github-actions
  namespace: virons-api
roleRef:
  kind: Role
  name: api-deployer
  apiGroup: rbac.authorization.k8s.io
```

### Pod Security Standards
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: virons-api
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-gateway-policy
  namespace: virons-api
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: virons-data
    ports:
    - protocol: TCP
      port: 5432
```

## Secrets Management

### External Secrets Operator
```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: virons-api
spec:
  provider:
    aws:
      service: SecretsManager
      region: eu-central-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
  namespace: virons-api
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: db-credentials
  data:
  - secretKey: host
    remoteRef:
      key: virons/demo/database
      property: host
  - secretKey: password
    remoteRef:
      key: virons/demo/database
      property: password
```

## Monitoring

### Prometheus & Grafana
```yaml
# ServiceMonitor for Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-gateway
  namespace: virons-api
spec:
  selector:
    matchLabels:
      app: api-gateway
  endpoints:
  - port: metrics
    interval: 30s
```

### Container Insights
```bash
# Enable Container Insights
aws eks update-cluster-config \
  --name virons-demo \
  --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'
```

## Auto-scaling

### HPA
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway-hpa
  namespace: virons-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-gateway
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Cluster Autoscaler
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: cluster-autoscaler
  namespace: kube-system
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    spec:
      serviceAccountName: cluster-autoscaler
      containers:
      - image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.29.0
        name: cluster-autoscaler
        command:
        - ./cluster-autoscaler
        - --cloud-provider=aws
        - --namespace=kube-system
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/virons-demo
```

## GitOps (ArgoCD)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: virons-api
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/virons-fintech/virons-services
    targetRevision: main
    path: k8s/api
  destination:
    server: https://kubernetes.default.svc
    namespace: virons-api
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Quick Reference

```bash
# Cluster management
eksctl create cluster -f cluster.yaml
kubectl get nodes
kubectl get pods -A

# Deploy application
kubectl apply -f deployment.yaml
kubectl rollout status deployment/api-gateway -n virons-api

# Logs
kubectl logs -f deployment/api-gateway -n virons-api

# Scale
kubectl scale deployment/api-gateway --replicas=5 -n virons-api

# Secrets
kubectl create secret generic db-creds --from-literal=password=xxx -n virons-api
```

---
**Version**: 1.0.0
**Last Updated**: February 25, 2026
**Virons AI Platform**

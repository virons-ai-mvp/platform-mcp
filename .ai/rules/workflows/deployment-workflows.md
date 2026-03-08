# Deployment Workflows

## Build & Push

```bash
# Authenticate to ECR
aws ecr get-login-password --region eu-central-1 | \
  docker login --username AWS --password-stdin \
  412179655775.dkr.ecr.eu-central-1.amazonaws.com

# Build and push
docker build -t virons/{service}:{tag} .
docker tag virons/{service}:{tag} \
  412179655775.dkr.ecr.eu-central-1.amazonaws.com/virons/{service}:{tag}
docker push 412179655775.dkr.ecr.eu-central-1.amazonaws.com/virons/{service}:{tag}
```

## Deploy to EKS

```bash
# Set context
aws eks update-kubeconfig --name virons-mvp --region eu-central-1

# Apply (requires human approval)
kubectl apply -f k8s/ -n virons-{namespace}

# Verify rollout
kubectl rollout status deployment/{service} -n virons-{namespace}
```

## Rollback

```bash
kubectl rollout undo deployment/{service} -n virons-{namespace}
kubectl rollout status deployment/{service} -n virons-{namespace}
```

## Health Check

```bash
kubectl get pods -n virons-{namespace}
kubectl logs -f deployment/{service} -n virons-{namespace}
```

## Change Window (Production)

- Tue–Thu 10:00–16:00 CET only
- Rollback plan must be documented before deployment
- Monitor for 30 minutes post-deployment

## Node Groups

- `ng-general` (m6i.large Spot): ingestion, forensic, blockchain, api
- `ng-inference` (m6i.xlarge On-Demand): ml namespace only

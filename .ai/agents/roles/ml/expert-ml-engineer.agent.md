# Expert ML Engineer Agent
**Version**: 1.0.0
**Role**: ML Operations, Model Training & Deployment
**Stack**: SageMaker, Bedrock, MLflow, Feature Store
**Risk Level**: HIGH (0.85)

## Purpose
Design and operate ML infrastructure for Virons AI platform with focus on model lifecycle, monitoring, and compliance.

## ML Architecture

### Current Stack (Bedrock)
```text
User Request → API Gateway → Bedrock Runtime API → Claude 3.5 Sonnet
                                                          ↓
                                                    Guardrails
                                                          ↓
                                                      Response
```

### Future Stack (Custom Models)
```text
Data → Feature Store → SageMaker Training → Model Registry → SageMaker Endpoint
                            ↓                      ↓
                       Experiments            Monitoring
```

## AWS Bedrock Integration

### Model Invocation
```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='eu-central-1')

def invoke_claude(prompt: str, max_tokens: int = 1024) -> str:
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
        body=body
    )

    result = json.loads(response['body'].read())
    return result['content'][0]['text']
```

### Embeddings
```python
def generate_embeddings(text: str) -> list[float]:
    body = json.dumps({
        "inputText": text
    })

    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v1',
        body=body
    )

    result = json.loads(response['body'].read())
    return result['embedding']
```

### Guardrails
```python
def invoke_with_guardrails(prompt: str) -> str:
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    })

    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
        body=body,
        guardrailIdentifier='virons-content-filter',
        guardrailVersion='1'
    )

    return json.loads(response['body'].read())
```

## SageMaker (Future Custom Models)

### Training Job
```python
import sagemaker
from sagemaker.estimator import Estimator

role = 'arn:aws:iam::412179655775:role/SageMakerExecutionRole'

estimator = Estimator(
    image_uri='763104351884.dkr.ecr.eu-central-1.amazonaws.com/pytorch-training:2.0.0-gpu-py310',
    role=role,
    instance_count=1,
    instance_type='ml.g5.xlarge',
    volume_size=50,
    max_run=3600,
    output_path='s3://virons-ml-artifacts/models',
    base_job_name='virons-model-training'
)

estimator.fit({
    'training': 's3://virons-ml-data/train',
    'validation': 's3://virons-ml-data/val'
})
```

### Model Deployment
```python
from sagemaker.model import Model
from sagemaker.predictor import Predictor

model = Model(
    image_uri='763104351884.dkr.ecr.eu-central-1.amazonaws.com/pytorch-inference:2.0.0-gpu-py310',
    model_data=estimator.model_data,
    role=role
)

predictor = model.deploy(
    initial_instance_count=2,
    instance_type='ml.g5.xlarge',
    endpoint_name='virons-model-endpoint'
)
```

## Feature Store

### Feature Group
```python
from sagemaker.feature_store.feature_group import FeatureGroup

feature_group = FeatureGroup(
    name='virons-user-features',
    sagemaker_session=sagemaker_session
)

feature_group.create(
    s3_uri='s3://virons-feature-store',
    record_identifier_name='user_id',
    event_time_feature_name='timestamp',
    role_arn=role,
    enable_online_store=True
)
```

### Feature Ingestion
```python
import pandas as pd

features = pd.DataFrame({
    'user_id': ['user1', 'user2'],
    'total_conversations': [10, 5],
    'avg_tokens_per_message': [150, 200],
    'timestamp': [1708826400, 1708826400]
})

feature_group.ingest(
    data_frame=features,
    max_workers=3,
    wait=True
)
```

## Model Monitoring

### CloudWatch Metrics
```python
import boto3

cloudwatch = boto3.client('cloudwatch', region_name='eu-central-1')

def log_model_metrics(endpoint_name: str, latency: float, tokens: int):
    cloudwatch.put_metric_data(
        Namespace='Virons/ML',
        MetricData=[
            {
                'MetricName': 'ModelLatency',
                'Value': latency,
                'Unit': 'Milliseconds',
                'Dimensions': [
                    {'Name': 'EndpointName', 'Value': endpoint_name}
                ]
            },
            {
                'MetricName': 'TokensGenerated',
                'Value': tokens,
                'Unit': 'Count',
                'Dimensions': [
                    {'Name': 'EndpointName', 'Value': endpoint_name}
                ]
            }
        ]
    )
```

### Model Quality Monitoring
```python
from sagemaker.model_monitor import ModelQualityMonitor

monitor = ModelQualityMonitor(
    role=role,
    instance_count=1,
    instance_type='ml.m5.xlarge',
    volume_size_in_gb=20,
    max_runtime_in_seconds=3600
)

monitor.create_monitoring_schedule(
    endpoint_input=predictor.endpoint_name,
    output_s3_uri='s3://virons-ml-monitoring',
    schedule_cron_expression='cron(0 * * * ? *)'  # Hourly
)
```

## MLOps Pipeline

### MLflow Tracking
```python
import mlflow

mlflow.set_tracking_uri('s3://virons-mlflow')
mlflow.set_experiment('virons-model-training')

with mlflow.start_run():
    mlflow.log_param('learning_rate', 0.001)
    mlflow.log_param('batch_size', 32)
    mlflow.log_metric('accuracy', 0.95)
    mlflow.log_metric('loss', 0.05)
    mlflow.pytorch.log_model(model, 'model')
```

### Model Registry
```python
from sagemaker.model_registry import ModelPackageGroup

model_package_group = ModelPackageGroup(
    model_package_group_name='virons-models',
    model_package_group_description='Virons AI models'
)

model_package_group.create()
```

## Cost Optimization

### Bedrock Cost Tracking
```python
def calculate_bedrock_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    pricing = {
        'claude-3-5-sonnet': {'input': 0.003, 'output': 0.015},  # per 1K tokens
        'claude-3-haiku': {'input': 0.00025, 'output': 0.00125}
    }

    cost = (input_tokens / 1000 * pricing[model]['input'] +
            output_tokens / 1000 * pricing[model]['output'])
    return cost
```

### SageMaker Cost Optimization
- Use Spot instances for training (70% savings)
- Auto-scaling for inference endpoints
- Serverless inference for low-traffic models
- Model compression and quantization

## Compliance

**EU AI Act**:
- Model risk assessment
- Documentation and transparency
- Human oversight mechanisms
- Bias testing and mitigation

**GDPR**:
- Data minimization in training
- Right to explanation
- Model versioning for auditability

**BaFin**:
- Model validation procedures
- Change management
- Audit trails

## Quick Reference

```bash
# Bedrock
aws bedrock list-foundation-models --region eu-central-1
aws bedrock-runtime invoke-model --model-id anthropic.claude-3-5-sonnet-20241022-v2:0 --body file://input.json output.json

# SageMaker
aws sagemaker list-training-jobs
aws sagemaker list-endpoints
aws sagemaker describe-endpoint --endpoint-name virons-model-endpoint

# Monitoring
aws cloudwatch get-metric-statistics \
  --namespace Virons/ML \
  --metric-name ModelLatency \
  --start-time 2026-02-25T00:00:00Z \
  --end-time 2026-02-25T23:59:59Z \
  --period 3600 \
  --statistics Average
```

---
**Version**: 1.0.0
**Last Updated**: February 25, 2026
**Virons AI Platform**

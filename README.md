# aws-resource-exporter

## Metrics

- Running instances count
- Active spot instance requests count

## Package

```
pip install -r src/requirements.txt -t src
```

```
aws cloudformation package --template-file template.yaml --output-template-file aws-resource-exporter.yaml --s3-bucket <YOUR_S3_BUCKET>
```

## Deploy

```
aws cloudformation deploy --template-file aws-resource-exporter.yaml --stack-name aws-resource-exporter --capabilities=CAPABILITY_IAM
```

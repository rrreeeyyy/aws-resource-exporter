from boto3 import client, resource
from collections import Counter
from itertools import groupby
from prometheus_client import Gauge, generate_latest

def handler(event, context):
    instance_gauge = Gauge('aws_instance_count', 'AWS instance count by instance_type', ['instance_type'])
    spot_instance_guage = Gauge('aws_spot_instance_count', 'AWS spot instance count by instance_type', ['instance_type'])
    _aws_ec2_instance_count(instance_gauge)
    _aws_ec2_spot_instance_requests_count(spot_instance_guage)

    headers = {
        'Content-Type': 'text/plain'
    }
    return {'statusCode': 200, 'body': generate_latest().decode('utf-8'), 'headers': headers}

def _aws_ec2_instance_count(gauge):
    ec2 = resource('ec2')
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    counter = Counter([instance.instance_type for instance in instances])

    for instance_type, count in counter.most_common():
        gauge.labels(instance_type).inc(count)

def _aws_ec2_spot_instance_requests_count(gauge):
    ec2 = client('ec2')
    instances = ec2.describe_spot_instance_requests(Filters=[{'Name': 'state', 'Values': ['active']}])['SpotInstanceRequests']
    counter = Counter([instance['LaunchSpecification']['InstanceType'] for instance in instances])

    for instance_type, count in counter.most_common():
        gauge.labels(instance_type).inc(count)

if __name__ == '__main__':
    print(handler(None, None))

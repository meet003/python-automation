import boto3


ec2_client_1 = boto3.client('ec2',region_name="us-east-1" )
ec2_resource_1 = boto3.resource('ec2',region_name="us-east-1" )
instance_ids_1 = []

instances  = ec2_client_1.describe_instances()['Reservations']
for res in instances:
    instance = res['Instances']
    for ins in instance:
        instance_ids_1.append(ins['InstanceId'])

print(instance_ids_1)


response = ec2_resource_1.create_tags(
    Resources=instance_ids_1,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)
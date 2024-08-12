import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2',region_name="us-east-1" )
ec2_resource = boto3.resource('ec2',region_name="us-east-1" )


instance_id = "hbfcjfhbv"

ec2_client.describe_volumes(
    Filters=[
        {
            'Name':'attachment.instance-id',
            'Values':[instance_id]
        }
    ]
)

instance_volume = volumes['Volumes'][0]
print(instance_volume)

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
        {
        'Name':'volume-id',
        'Values': [instance_volume['VolumeID']]

        }
        
    ]
)

latest_snapshot = sorted(snapshots['Snapshots'],key=itemgetter('StartTime'),reverse=True)[0]
print(latest_snapshot['StartTime'])

ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone="us-east-1",
    TagSpecifications=[
        {
        'ResourceType':'volume',
        'Tags':[
            {
            'key':'Name',
            'Value':'prod'
            }
        ]
        }
    ]
)
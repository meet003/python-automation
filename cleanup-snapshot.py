import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2',region_name="us-east-1" )

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self']
)

sorted_by_data = sorted(snapshots['Snapshots'],key=itemgetter('StartTime'),reverse=True)
# for snap in sorted_by_data:
#     print(snap['StartTime'])

# for snap in sorted_by_data[1:]:
#     print(snap['StartTime'])

# print(snapshots['Snapshots'])

#------------deletion logic
for snap in sorted_by_data[1:]:
   response = ec2_client.delete_snapshot(
      SnapshotId = snap['SnapshotId']
   )
   print(response)
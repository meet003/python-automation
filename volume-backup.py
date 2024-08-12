import boto3

ec2_client = boto3.client('ec2',region_name="us-east-1" )

volumes = ec2_client.describe_volumes()
# print(volumes)

for volume in volumes['Volumes']:  
    print(volume['VolumeId']);
    new_snapshot = ec2_client.create_snapshot(
        VolumeId=volume['VolumeId']
    )
    print(new_snapshot)


# #schedule task
# import boto3
# import schedule

# ec2_client = boto3.client('ec2',region_name="us-east-1" )


# def create_volume_snapshots():
#     volumes = ec2_client.describe_volumes()
#     # print(volumes)

#     for volume in volumes['Volumes']:  
#         print(volume['VolumeId']);
#         new_snapshot = ec2_client.create_snapshot(
#             VolumeId=volume['VolumeId']
#         )
#         print(new_snapshot)

# schedule.every().day.do(create_volume_snapshots)

# while True:
#     schedule.run_pending()
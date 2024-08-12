import boto3
import schedule

ec2_client = boto3.client('ec2',region_name="us-east-1" )

def check_instance_status():
    instances  = ec2_client.describe_instances()
    for reservation in instances['Reservations']:
        instance = reservation['Instances']
        for instanceCheck in instance:
            print(f"insyance {instanceCheck['InstanceId']}  {instanceCheck['State']['Name']}")
        # print(reservation['Instances'])
    # print(instances)
 
schedule.every(5).seconds.do(check_instance_status)

while True:
    schedule.run_pending()